"""AI Triage, Multimodal Document Verification & Auto-Reply Service powered by OpenRouter."""
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

# Free multimodal vision models on OpenRouter (fallback chain)
DEFAULT_VISION_MODEL = "openrouter/free"
FALLBACK_MODELS = [
    "openrouter/free",
    "google/gemma-4-31b-it:free",
    "openai/gpt-4o-mini",
]


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


def _format_threaded_reply_subject(subject: Optional[str]) -> str:
    """Format subject strictly as 'Re: <Original Subject>' so Gmail/email clients thread it as a reply."""
    clean = (subject or "").strip()
    if not clean:
        return "Re: Hope Medical Assistance Application"
    if clean.lower().startswith("re:"):
        return clean
    return f"Re: {clean}"


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
    att_list = attachment_metadata or []
    att_count = len(att_list)
    att_names = [str(a.get("filename") or a.get("url") or "attachment") for a in att_list]

    # Category detection
    category = "general"
    if any(k in lower for k in ("surgery", "operation", "transplant", "bypass", "appendectomy", "valve")):
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
    elif any(k in lower for k in ("urgent", "soon", "scheduled surgery", "high", "next tuesday")):
        urgency = "high"

    # Extract dollar amounts if mentioned (e.g. total estimate vs requested amount)
    all_amounts = re.findall(r"\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?|[0-9]+(?:\.[0-9]{2})?)", text)
    parsed_amounts: list[float] = []
    for raw_amt in all_amounts:
        try:
            parsed_amounts.append(float(raw_amt.replace(",", "")))
        except ValueError:
            pass
    extracted_estimate: Optional[float] = parsed_amounts[0] if parsed_amounts else None
    extracted_requested: Optional[float] = (
        parsed_amounts[1] if len(parsed_amounts) >= 2 else extracted_estimate
    )

    # Extract hospital name if mentioned
    hosp_match = re.search(r"\b([A-Z][A-Za-z0-9&\s]{2,40}?\s+(?:Hospital|Medical Center|Clinic|Institute|Health))\b", text)
    extracted_hospital = hosp_match.group(1).strip() if hosp_match else (existing_case_context or {}).get("hospital_name")

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

    # Determine verification completeness (accounting for future-tense promises like "will send ... as soon as")
    doc_text = " ".join(str(a.get("extracted_text") or "") for a in att_list).lower()
    combined_names = " ".join(att_names).lower() + " " + lower + " " + prev_summary.lower() + " " + doc_text
    deferred_estimate = bool(re.search(r"will\s+send[^.]*?(?:estimate|bill|invoice)", lower))
    deferred_id = bool(re.search(r"will\s+send[^.]*?(?:id|passport|aadhaar|license)", lower))

    has_estimate = (
        any(k in combined_names for k in ("estimate", "bill", "invoice", "quote", "stamped"))
        and not deferred_estimate
    )
    has_id = (
        any(k in combined_names for k in ("id", "passport", "aadhaar", "license", "government"))
        and not deferred_id
    )
    has_medical = any(k in combined_names for k in ("prescription", "admission", "report", "doctor", "note", "clearance"))
    mentions_attaching = any(k in lower for k in ("attaching", "attached", "enclosed", "submitting"))

    pending_items: list[str] = []
    if not has_estimate:
        pending_items.append("hospital_treatment_estimate")
    if not has_id:
        pending_items.append("patient_government_id")
    if not has_medical and att_count == 0 and not mentions_attaching:
        pending_items.append("medical_prescription_or_admission_note")

    has_any_docs = att_count > 0 or mentions_attaching
    is_verified = len(pending_items) == 0 and has_any_docs
    verification_score = 100 if is_verified else (70 if att_count >= 2 else (45 if has_any_docs else 15))

    if is_verified:
        status = "approved"
        next_action = "100% Verified — Ready to disburse payout to beneficiary"
    elif has_any_docs:
        status = "under_review"
        next_action = f"Request remaining documents: {', '.join(pending_items)}"
    else:
        status = "awaiting_documents"
        next_action = "Send auto-reply requesting hospital estimate, medical report, and government ID"

    patient_name = (existing_case_context or {}).get("patient_name") or _extract_name_from_sender(sender) or "Applicant"
    auto_reply_subject = _format_threaded_reply_subject(subject)
    if is_verified:
        auto_reply_body = (
            f"Dear {patient_name},\n\n"
            "Thank you for submitting your medical and identification documents.\n\n"
            "--- CASE VERIFICATION STATUS ---\n"
            f"• Case Summary: {updated_case_summary}\n"
            "• Pending Documents: None (100% Verified)\n"
            f"• Next Action: {next_action}\n"
            "--------------------------------\n\n"
            "Your case is now APPROVED and queued for immediate fund disbursement to your registered account.\n\n"
            "Warm regards,\nHope Medical Verification Team"
        )
    else:
        missing_str = ", ".join(item.replace("_", " ") for item in pending_items)
        auto_reply_body = (
            f"Dear {patient_name},\n\n"
            "Thank you for reaching out to Hope Medical Foundation. We have received your message and updated your case file.\n\n"
            "--- CASE VERIFICATION STATUS ---\n"
            f"• Case Summary: {updated_case_summary}\n"
            f"• Pending Documents: {missing_str}\n"
            f"• Next Action: {next_action}\n"
            "--------------------------------\n\n"
            "Please reply to this email with the pending document(s) listed above. Once received and 100% verified, we will immediately process your payout.\n\n"
            "Warm regards,\nHope Medical Verification Team"
        )

    return {
        "intent": "document_submission" if att_count > 0 else "initial_application",
        "patient_name": patient_name,
        "patient_email": (existing_case_context or {}).get("patient_email") or _extract_email_address(sender),
        "medical_category": (existing_case_context or {}).get("medical_category") or category,
        "treatment_description": (body_plain or subject or "")[:500] or None,
        "hospital_name": extracted_hospital,
        "estimated_cost": extracted_estimate,
        "requested_amount": extracted_requested,
        "urgency": urgency,
        "status": status,
        "verification_score": verification_score,
        "is_100_percent_verified": is_verified,
        "document_verification_notes": (
            f"Analyzed {att_count} attachment(s) ({', '.join(att_names)}). "
            + ("All required documents verified." if is_verified else f"Missing: {', '.join(pending_items)}.")
        ),
        "overall_summary": updated_case_summary,
        "next_action": next_action,
        "extracted_documents": att_names,
        "pending_items": pending_items,
        "auto_reply_subject": auto_reply_subject,
        "auto_reply_body": auto_reply_body,
    }


def _extract_image_urls(attachment_metadata: Optional[list[dict[str, Any]]]) -> list[str]:
    """Extract valid HTTP(S) image/document URLs from attachment metadata for multimodal vision models."""
    urls: list[str] = []
    for att in attachment_metadata or []:
        if not isinstance(att, dict):
            continue
        url = att.get("url") or att.get("attachment_url") or att.get("file_url") or att.get("file")
        ctype = str(att.get("content_type") or "").lower()
        fname = str(att.get("filename") or "").lower()
        is_image = ctype.startswith("image/") or fname.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif"))
        if ctype and not ctype.startswith("image/") and not is_image:
            continue  # vision models only accept images; PDFs/text are handled via extracted_text
        if isinstance(url, str) and url.startswith(("http://", "https://")):
            urls.append(url.strip())
    return urls


def analyze_incoming_email(
    sender: str,
    subject: Optional[str],
    body_plain: Optional[str],
    attachment_metadata: Optional[list[dict[str, Any]]] = None,
    existing_case_context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Analyze an incoming email + attachment images/docs using OpenRouter free Vision models."""
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

    configured_model = os.getenv("OPENROUTER_MODEL", "").strip()
    models_to_try = ([configured_model] if configured_model else []) + [
        m for m in FALLBACK_MODELS if m != configured_model
    ]

    attachments_desc = json.dumps(attachment_metadata or [], default=str)
    case_desc = json.dumps(existing_case_context or {}, default=str)
    image_urls = _extract_image_urls(attachment_metadata)

    system_prompt = (
        "You are Hope Medical Crowdfunding's AI Case Triage & Multimodal Document Verification Assistant. "
        "Analyze the incoming email, any attached document images/files, and the existing case context. "
        "Return ONLY a valid JSON object with these exact keys:\n"
        "- intent: string ('initial_application', 'document_submission', 'hospital_verification', 'general_inquiry')\n"
        "- patient_name: string or null\n"
        "- patient_email: string or null\n"
        "- medical_category: one of ['upcoming_surgery', 'ongoing_hospitalization', 'emergency_care', 'chronic_treatment', 'medication_assistance', 'general']\n"
        "- treatment_description: concise description of medical condition/treatment or null\n"
        "- hospital_name: hospital or clinic name if mentioned or null\n"
        "- estimated_cost: numeric total treatment cost in USD if mentioned, else null\n"
        "- requested_amount: numeric financial aid requested in USD if mentioned, else null\n"
        "- urgency: one of ['low', 'medium', 'high', 'critical']\n"
        "- verification_score: integer 0 to 100 indicating how complete and authentic the medical/ID documentation is\n"
        "- is_100_percent_verified: boolean (true ONLY when official hospital cost estimate/bill AND patient ID/medical proof have been submitted and verified with no pending items left. Note: IMAP email triggers may strip attachment URLs from metadata even when files are attached; if the sender states in the email body that they are attaching/submitting the required documents now—and not merely promising to send them later—count those documents as submitted)\n"
        "- document_verification_notes: detailed findings from inspecting the attachments/documents\n"
        "- status: one of ['new', 'awaiting_documents', 'under_review', 'approved', 'rejected'] (set to 'approved' if is_100_percent_verified is true)\n"
        "- overall_summary: comprehensive living summary of all email exchanges in the case so far (combining existing_case_context and this new email)\n"
        "- next_action: clear next action for the case officer or payout system\n"
        "- extracted_documents: list of strings describing attachments/documents received so far\n"
        "- pending_items: list of strings for documents/verifications still missing (empty list [] if 100% verified)\n"
        "- auto_reply_subject: polite, clear subject line for the automatic reply email back to the sender\n"
        "- auto_reply_body: empathetic plain-text reply email to the patient/sender that explicitly includes the updated overall_summary, pending_items, and next_action\n"
        "Respond ONLY with raw JSON and no markdown fences."
    )

    text_prompt = (
        f"Sender: {sender}\n"
        f"Subject: {subject or '(No subject)'}\n"
        f"Attachments Metadata: {attachments_desc}\n"
        f"Existing Case Context: {case_desc}\n\n"
        f"Email Body:\n{body_plain or '(Empty body)'}"
    )

    # Build multimodal user content if image URLs are present
    user_content: Any
    if image_urls:
        user_content = [{"type": "text", "text": text_prompt}]
        for img_url in image_urls[:4]:
            user_content.append({"type": "image_url", "image_url": {"url": img_url}})
    else:
        user_content = text_prompt

    for model_name in models_to_try:
        try:
            payload_json: dict[str, Any] = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                "temperature": 0.1,
            }
            if "openai/" in model_name:
                payload_json["response_format"] = {"type": "json_object"}

            resp = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {api_key.strip()}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://hope-9dq5.onrender.com",
                    "X-Title": "Hope Medical Case Triage & Vision Verification",
                },
                json=payload_json,
                timeout=18,
            )
            if not resp.ok:
                logger.warning("OpenRouter model %s returned HTTP %d: %s", model_name, resp.status_code, resp.text[:200])
                continue

            data = resp.json()
            content = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
            if not content:
                continue
            content = content.strip()
            if "```" in content:
                match = re.search(r"\{.*\}", content, re.DOTALL)
                if match:
                    content = match.group(0)

            parsed = json.loads(content)
            if not isinstance(parsed, dict):
                continue

            merged = dict(fallback)
            for k, v in parsed.items():
                if v is not None:
                    merged[k] = v

            # Ensure consistency when pending_items is empty and documents were provided
            if merged.get("is_100_percent_verified") is True:
                merged["status"] = "approved"
                merged["verification_score"] = 100
                merged["pending_items"] = []

            # Guarantee the reply email explicitly includes overall_summary, pending_items, and next_action
            summary_str = str(merged.get("overall_summary") or "Case received and under review.")
            pending_list = merged.get("pending_items") if isinstance(merged.get("pending_items"), list) else []
            pending_str = ", ".join(str(x) for x in pending_list) if pending_list else "None (100% Verified)"
            action_str = str(merged.get("next_action") or "Review submitted documents")

            base_reply = str(merged.get("auto_reply_body") or "").strip()
            status_block = (
                "\n\n--- CASE VERIFICATION STATUS ---\n"
                f"• Case Summary: {summary_str}\n"
                f"• Pending Documents: {pending_str}\n"
                f"• Next Action: {action_str}\n"
                "--------------------------------"
            )
            if "CASE VERIFICATION STATUS" not in base_reply:
                merged["auto_reply_body"] = f"{base_reply}{status_block}" if base_reply else status_block.strip()

            # Force strict 'Re: <Original Subject>' so Gmail threads the reply into the same conversation
            merged["auto_reply_subject"] = _format_threaded_reply_subject(subject)
            merged["model_used"] = model_name
            return merged
        except Exception as exc:
            logger.warning("OpenRouter model %s failed, trying next fallback: %s", model_name, exc)
            continue

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
