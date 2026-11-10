"""AI Triage, Multimodal Document Verification & Auto-Reply Service powered by OpenRouter."""
import json
import logging
import os
import re
from datetime import date
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
    all_amounts = re.findall(r"(?:\$|\bUSD\s*)\s*([0-9]+(?:,[0-9]{3})*(?:\.[0-9]{1,2})?)", text)
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
    # Questions about missing documents and living summaries are not submitted
    # evidence. Only use actual attachment names/content for this receipt hint.
    combined_names = " ".join(att_names).lower().replace('_', ' ').replace('-', ' ') + " " + doc_text
    deferred_estimate = bool(re.search(r"will\s+send[^.]*?(?:estimate|bill|invoice)", lower))
    deferred_id = bool(re.search(r"will\s+send[^.]*?(?:id|passport|aadhaar|license)", lower))

    has_estimate = (
        any(k in combined_names for k in ("estimate", "bill", "invoice", "quote", "stamped"))
        and not deferred_estimate
    )
    has_id = (
        bool(re.search(r"\b(?:id|identification|passport|aadhaar|license|government)\b", combined_names))
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
    # Keyword matches cannot establish document authenticity or approve spending.
    is_verified = False
    verification_score = 70 if att_count >= 2 else (45 if has_any_docs else 15)

    if has_any_docs:
        status = "under_review"
        next_action = f"Request remaining documents: {', '.join(pending_items)}" if pending_items else "Review submitted documents"
    else:
        status = "awaiting_documents"
        next_action = "Send auto-reply requesting hospital estimate, medical report, and government ID"

    patient_name = (existing_case_context or {}).get("patient_name") or _extract_name_from_sender(sender) or "Applicant"
    auto_reply_subject = _format_threaded_reply_subject(subject)
    readable_items = {
        'hospital_treatment_estimate': 'the hospital’s treatment estimate or bill',
        'patient_government_id': 'the patient’s government ID',
        'medical_prescription_or_admission_note': 'a medical prescription or admission note',
    }
    if pending_items:
        missing = '; '.join(readable_items.get(item, item.replace('_', ' ')) for item in pending_items)
        reply = f"To continue reviewing your application, please reply with {missing}."
    else:
        reply = "We have received the documents you mentioned. Our team needs to review them before confirming approval."
    if att_count:
        acknowledgement = f"Thank you for sending {', '.join(att_names)}."
    else:
        acknowledgement = "Thank you for your message about medical assistance."
    auto_reply_body = (
        f"Hi {patient_name},\n\n{acknowledgement} {reply}\n\n"
        "Warm regards,\nHope Medical Team"
    )

    return {
        "model_used": "heuristic_fallback",
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
            + ("Documents require review." if not pending_items else f"Missing: {', '.join(pending_items)}.")
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


def _analysis_failure(sender: str, subject: Optional[str], reason: str) -> dict[str, Any]:
    return {
        'analysis_status': 'failed',
        'failure_reason': reason,
        'model_used': None,
        'patient_email': _extract_email_address(sender),
        'status': 'under_review',
        'is_100_percent_verified': False,
        'overall_summary': 'Document analysis could not be completed; another review attempt is required.',
        'next_action': 'Retry document analysis when the analysis service is available',
        'pending_items': ['document_analysis_retry'],
        'auto_reply_subject': _format_threaded_reply_subject(subject),
        'auto_reply_body': (
            'Dear Applicant,\n\n'
            'We have received your email. Unfortunately, we could not complete the document review '
            'because our analysis service is currently unavailable. No approval or payment decision '
            'has been made from this attempt.\n\n'
            'Please try again later by replying to this email with the relevant documents attached.\n\n'
            'Kind regards,\nHope Medical Assistance Team'
        ),
    }


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
    if os.getenv("DISABLE_OPENROUTER_IN_TESTS") == "1":
        return fallback
    if not api_key:
        logger.error("Document analysis unavailable: OpenRouter API key is not configured")
        return _analysis_failure(sender, subject, 'analysis_not_configured')

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
        "- is_100_percent_verified: boolean (true ONLY when official hospital cost estimate/bill AND patient ID/medical proof have been submitted and verified with no pending items left. Never treat filenames or a sender’s claim of attachment as verification; if actual readable evidence is unavailable, keep the case under_review)\n"
        "- document_verification_notes: detailed findings from inspecting the attachments/documents\n"
        "- document_checks: list of objects, one per supplied attachment. Each object MUST include document_type ('medical_record', 'cost_estimate', or 'government_id'), attachment_index (zero-based index in Attachments Metadata), verdict ('verified', 'unreadable', 'mismatch', or 'invalid'), patient_name, issuer, document_date (YYYY-MM-DD), and evidence_text (an exact excerpt READ from that attachment, never the email). Medical records also require diagnosis and clinician. Cost estimates require numeric amount and ISO currency. Government ID requires id_type and id_last_four (only last four characters; never reproduce the full ID). Only verified means the attachment is readable, internally consistent, and supports its claimed type. Do not label a medical prescription as a bill or identity document. One attachment can support only one document type; request separate files for combined bundles. Never invent an excerpt or document details. If an attachment is not available/readable, mark unreadable. Do not repeat old evidence as a current attachment; existing_case_context.verification_evidence contains previously checked documents.\n"
        "- verification_issues: list of strings for mismatched patient details, invalid or stale documents, suspicious alterations, or other unresolved checks; empty only if none found\n"
        "- status: one of ['new', 'awaiting_documents', 'under_review', 'rejected']. The backend computes approval from document evidence; never decide approval from confidence alone\n"
        "- overall_summary: comprehensive living summary of all email exchanges in the case so far (combining existing_case_context and this new email)\n"
        "- next_action: clear next action for the case officer or payout system\n"
        "- extracted_documents: list of strings describing attachments/documents received so far\n"
        "- pending_items: list of strings for documents/verifications still missing (empty list [] if 100% verified)\n"
        "- auto_reply_subject: polite, clear subject line for the automatic reply email back to the sender\n"
        "- auto_reply_body: natural, empathetic plain-text reply addressing the latest message using case history. Ask only for genuinely missing information. Do not paste internal summaries, scores, field names, or status-report templates. Never claim the application is approved or request PayPal details. The backend adds factual payment instructions after document checks pass. Never say funds were sent\n"
        "Respond ONLY with raw JSON and no markdown fences."
    )

    text_prompt = (
        f"Review date: {date.today().isoformat()}\n"
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
            if (not isinstance(parsed, dict)
                    or not isinstance(parsed.get('document_checks'), list)
                    or not isinstance(parsed.get('verification_issues'), list)
                    or not isinstance(parsed.get('auto_reply_body'), str)
                    or not parsed['auto_reply_body'].strip()):
                logger.warning("OpenRouter model %s returned an incomplete analysis", model_name)
                continue

            merged = dict(fallback)
            for k, v in parsed.items():
                if v is not None:
                    merged[k] = v

            # Force strict 'Re: <Original Subject>' so Gmail threads the reply into the same conversation
            merged["auto_reply_subject"] = _format_threaded_reply_subject(subject)
            merged["model_used"] = model_name
            merged["analysis_status"] = 'completed'
            return merged
        except Exception as exc:
            logger.warning("OpenRouter model %s failed, trying next fallback: %s", model_name, exc)
            continue

    logger.error("All configured document-analysis model attempts failed")
    return _analysis_failure(sender, subject, 'all_models_failed')


def to_decimal_or_none(val: Any) -> Optional[Decimal]:
    if val is None or val == "":
        return None
    try:
        cleaned = str(val).replace("$", "").replace(",", "").strip()
        d = Decimal(cleaned)
        return d.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return None
