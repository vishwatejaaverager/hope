"""AI Triage & Living Case Summary Service powered by OpenRouter."""
import json
import logging
import os
import re
from decimal import Decimal, InvalidOperation
from typing import Any, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_OPENROUTER_MODEL = "openai/gpt-4o-mini"


def get_openrouter_api_key() -> Optional[str]:
    return (
        os.getenv("OPENROUTER_API")
        or os.getenv("OPENROUTER_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )


def _extract_name_from_sender(sender: str) -> Optional[str]:
    if not sender:
        return None
    if "<" in sender:
        name_part = sender.split("<", 1)[0].strip().strip('"').strip("'")
        if name_part:
            return name_part
    user_part = sender.split("@", 1)[0].replace(".", " ").replace("_", " ").strip()
    return user_part.title() if user_part else None


def _extract_email_address(sender: str) -> str:
    if not sender:
        return ""
    if "<" in sender and ">" in sender:
        return sender.split("<", 1)[-1].split(">", 1)[0].strip()
    return sender.strip()


def _heuristic_fallback_analysis(
    sender: str,
    subject: Optional[str],
    body_plain: Optional[str],
    attachment_metadata: Optional[list[dict[str, Any]]],
    existing_case_context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Deterministic fallback when OpenRouter API is unavailable or disabled in unit tests."""
    text = f"{subject or ''}\n{body_plain or ''}".strip()
    lower = text.lower()
    att_count = len(attachment_metadata or [])
    att_names = [str(a.get("filename") or "attachment") for a in (attachment_metadata or [])]

    # Category detection
    category = "general"
    if any(k in lower for k in ("surgery", "operation", "transplant", "bypass", "appendectomy")):
        category = "upcoming_surgery"
    elif any(k in lower for k in ("admitted", "icu", "hospitalized", "hospitalization", "inpatient")):
        category = "ongoing_hospitalization"
    elif any(k in lower for k in ("emergency", "trauma", "accident", "urgent")):
        category = "emergency_care"
    elif any(k in lower for k in ("chemo", "dialysis", "cancer", "chronic", "therapy")):
        category = "chronic_treatment"
    elif any(k in lower for k in ("medication", "medicine", "insulin", "prescription", "drug")):
        category = "medication_assistance"

    # Urgency detection
    urgency = "medium"
    if any(k in lower for k in ("critical", "icu", "life-threatening", "emergency", "immediately")):
        urgency = "critical"
    elif any(k in lower for k in ("urgent", "soon", "scheduled surgery", "high")):
        urgency = "high"

    # Extract dollar amount if mentioned
    amount_match = re.search(r"\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?|[0-9]+(?:\.[0-9]{2})?)", text)
    extracted_amount: Optional[float] = None
    if amount_match:
        try:
            extracted_amount = float(amount_match.group(1).replace(",", ""))
        except ValueError:
            extracted_amount = None

    email_summary = (
        f"Received email '{subject or '(No subject)'}' from {sender}"
        + (f" with {att_count} attachment(s) ({', '.join(att_names)})." if att_count else ".")
    )

    prev_summary = (existing_case_context or {}).get("overall_summary") or ""
    if prev_summary:
        updated_case_summary = f"{prev_summary} | Update: {email_summary}"
    else:
        snippet = (body_plain or subject or "Medical assistance inquiry").strip()[:220]
        updated_case_summary = f"Patient inquiry ({category}): {snippet}"

    pending_items = ["hospital_treatment_estimate", "medical_report", "patient_id_proof"]
    if att_count > 0:
        pending_items = ["hospital_billing_verification"]

    status = "under_review" if att_count > 0 else "awaiting_documents"
    next_action = (
        "Verify submitted attachments with hospital billing department"
        if att_count > 0
        else "Request medical estimate and hospital verification documents from applicant"
    )

    return {
        "intent": "document_submission" if att_count > 0 else "assistance_application",
        "patient_name": (existing_case_context or {}).get("patient_name") or _extract_name_from_sender(sender),
        "patient_email": (existing_case_context or {}).get("patient_email") or _extract_email_address(sender),
        "medical_category": (existing_case_context or {}).get("medical_category") or category,
        "treatment_description": (body_plain or subject or "")[:500] or None,
        "hospital_name": (existing_case_context or {}).get("hospital_name"),
        "estimated_cost": extracted_amount,
        "requested_amount": extracted_amount,
        "urgency": urgency,
        "status": status,
        "summary": email_summary,
        "overall_summary": updated_case_summary,
        "next_action": next_action,
        "extracted_documents": att_names,
        "pending_items": pending_items,
    }


def analyze_incoming_email(
    sender: str,
    subject: Optional[str],
    body_plain: Optional[str],
    attachment_metadata: Optional[list[dict[str, Any]]] = None,
    existing_case_context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Analyze an incoming email using OpenRouter LLM and return structured triage & summary data."""
    fallback = _heuristic_fallback_analysis(
        sender=sender,
        subject=subject,
        body_plain=body_plain,
        attachment_metadata=attachment_metadata,
        existing_case_context=existing_case_context,
    )

    api_key = get_openrouter_api_key()
    if not api_key or os.getenv("DISABLE_OPENROUTER_IN_TESTS") == "1":
        return fallback

    model = os.getenv("OPENROUTER_MODEL", DEFAULT_OPENROUTER_MODEL).strip()
    attachments_desc = json.dumps(attachment_metadata or [], default=str)
    case_desc = json.dumps(existing_case_context or {}, default=str)

    system_prompt = (
        "You are Hope Medical Crowdfunding's AI Case Triage & Verification Assistant. "
        "Analyze the incoming email (and any existing case context) and return ONLY a valid JSON object "
        "with these exact keys:\n"
        "- intent: string ('initial_application', 'document_submission', 'hospital_verification', 'general_inquiry')\n"
        "- patient_name: string or null\n"
        "- patient_email: string or null\n"
        "- medical_category: one of ['upcoming_surgery', 'ongoing_hospitalization', 'emergency_care', 'chronic_treatment', 'medication_assistance', 'general']\n"
        "- treatment_description: concise description of medical condition/treatment or null\n"
        "- hospital_name: hospital or clinic name if mentioned or null\n"
        "- estimated_cost: numeric total treatment cost in USD if mentioned, else null\n"
        "- requested_amount: numeric financial aid requested in USD if mentioned, else null\n"
        "- urgency: one of ['low', 'medium', 'high', 'critical']\n"
        "- status: one of ['new', 'awaiting_documents', 'under_review', 'approved', 'rejected']\n"
        "- summary: 1-2 sentence summary of THIS email\n"
        "- overall_summary: comprehensive living summary of the entire case combining existing_case_context and this new email\n"
        "- next_action: clear next action for the case officer or AI\n"
        "- extracted_documents: list of strings describing attachments/documents received\n"
        "- pending_items: list of strings for documents/verifications still needed\n"
        "Respond ONLY with raw JSON and no markdown fences."
    )

    user_prompt = (
        f"Sender: {sender}\n"
        f"Subject: {subject or '(No subject)'}\n"
        f"Attachments: {attachments_desc}\n"
        f"Existing Case Context: {case_desc}\n\n"
        f"Email Body:\n{body_plain or '(Empty body)'}"
    )

    try:
        resp = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key.strip()}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://hope-9dq5.onrender.com",
                "X-Title": "Hope Medical Case Triage",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.1,
                "response_format": {"type": "json_object"},
            },
            timeout=12,
        )
        if not resp.ok:
            logger.warning("OpenRouter returned HTTP %d: %s", resp.status_code, resp.text[:200])
            return fallback

        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)

        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return fallback

        merged = dict(fallback)
        for k, v in parsed.items():
            if v is not None:
                merged[k] = v
        return merged
    except Exception as exc:
        logger.warning("OpenRouter analysis failed, using fallback analysis: %s", exc)
        return fallback


def to_decimal_or_none(val: Any) -> Optional[Decimal]:
    if val is None or val == "":
        return None
    try:
        cleaned = str(val).replace("$", "").replace(",", "").strip()
        d = Decimal(cleaned)
        return d.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return None

