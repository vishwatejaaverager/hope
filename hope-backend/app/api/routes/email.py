import logging
import os
import re
import secrets
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import requests

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, Response, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import verify_session_token, verify_webhook_secret
from app.db import get_db
from app.models import Case, EmailAttachment, IncomingEmail, OutgoingEmail
from app.services import ai_service, imap_service, smtp_service, case_workflow, approval_policy, attachment_service, document_review_store
from app.schemas.email import (
    IncomingEmailListItem,
    IncomingEmailPayload,
    IncomingEmailResponse,
    OutgoingEmailListItem,
    OutgoingEmailPayload,
    OutgoingEmailResponse,
    UpdateIncomingEmailPayload,
    UpdateOutgoingEmailStatusPayload,
)

logger = logging.getLogger(__name__)

DEFAULT_ZAPIER_OUTBOUND_HOOK = "https://hooks.zapier.com/hooks/catch/29325202/49x1egu/"
router = APIRouter(prefix="/api/v1/emails", tags=["emails"])


def _mask_email(email: Optional[str]) -> str:
    """Mask email for privacy-safe logging (e.g. j***@example.com)."""
    if not email or "@" not in email:
        return "unknown"
    user, domain = email.split("@", 1)
    masked_user = user[0] + "***" if len(user) > 0 else "***"
    return f"{masked_user}@{domain}"


def _mask_identifier(val: Optional[str]) -> str:
    """Mask message identifier for safe logging."""
    if not val:
        return "none"
    if len(val) <= 8:
        return val
    return f"{val[:4]}...{val[-4:]}"


def _resolve_case(
    db: Session,
    case_ref: Optional[str] = None,
    app_id: Optional[str] = None,
    sender_email: Optional[str] = None,
    thread_references: Optional[list[str]] = None,
) -> Optional[Case]:
    """Attempt to resolve a Case by explicit case_ref, application_id (UUID or case_number), or patient_email."""
    for candidate in (case_ref, app_id):
        if not candidate or candidate.strip().upper() == "GENERAL":
            continue
        cleaned = candidate.strip()
        try:
            val_uuid = uuid.UUID(cleaned)
            found = db.execute(select(Case).where(Case.id == val_uuid)).scalar_one_or_none()
            if found:
                return found
        except ValueError:
            pass
        found = db.execute(
            select(Case).where(func.lower(Case.case_number) == cleaned.lower())
        ).scalar_one_or_none()
        if found:
            return found

    # RFC References contains prior incoming IDs even if the immediate parent is
    # an outgoing message whose provider-generated ID is not stored locally.
    references = thread_references or []
    if references:
        linked = db.execute(select(IncomingEmail.case_id).where(
            IncomingEmail.message_id.in_(references), IncomingEmail.case_id.is_not(None))).scalars().all()
        unique = set(linked)
        if len(unique) == 1:
            return db.get(Case, unique.pop())
        if len(unique) > 1:
            return None

    if sender_email and "@" in sender_email:
        # Extract raw email if formatted like "Name <email@domain.com>"
        raw_email = sender_email.strip()
        if "<" in raw_email and ">" in raw_email:
            raw_email = raw_email.split("<", 1)[-1].split(">", 1)[0].strip()
        candidates = db.execute(select(Case).where(func.lower(Case.patient_email) == raw_email.lower())
                                .order_by(Case.created_at.desc()).limit(2)).scalars().all()
        if len(candidates) == 1:
            return candidates[0]
        # Never choose the latest case when a contact has multiple patients.

    return None


def _extract_provided_secret(
    request: Request,
    payload_secret: Optional[str],
    header_secret: Optional[str],
    zapier_secret: Optional[str],
    auth_header: Optional[str],
    query_secret: Optional[str],
    query_token: Optional[str],
) -> Optional[str]:
    """Find the webhook secret in headers, query params, or payload body."""
    direct = (
        header_secret
        or zapier_secret
        or auth_header
        or query_secret
        or query_token
        or payload_secret
    )
    if direct:
        return direct

    # Check case-insensitive raw request headers
    for key in (
        "x-webhook-secret",
        "x-zapier-secret",
        "webhook-secret",
        "authorization",
        "x-api-key",
        "email-webhook-secret",
        "email_webhook_secret",
    ):
        if key in request.headers:
            return request.headers[key]

    return None


def _authenticate_request(
    request: Request,
    payload_secret: Optional[str] = None,
    header_secret: Optional[str] = None,
    zapier_secret: Optional[str] = None,
    auth_header: Optional[str] = None,
    query_secret: Optional[str] = None,
    query_token: Optional[str] = None,
) -> bool:
    """Validate request using shared webhook secret or internal session token."""
    provided_secret = _extract_provided_secret(
        request=request,
        payload_secret=payload_secret,
        header_secret=header_secret,
        zapier_secret=zapier_secret,
        auth_header=auth_header,
        query_secret=query_secret,
        query_token=query_token,
    )
    if verify_webhook_secret(provided_secret):
        return True

    # Check for bearer session token
    if auth_header and auth_header.strip().lower().startswith("bearer "):
        token = auth_header.strip()[7:].strip()
        if verify_session_token(token) is not None:
            return True

    # Check for admin dashboard session cookie
    cookie_token = request.cookies.get("hope_admin_session")
    if cookie_token and verify_session_token(cookie_token) is not None:
        return True

    return False


@router.post(
    "/incoming",
    response_model=IncomingEmailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Receive incoming email webhook from Zapier",
)
def receive_incoming_email(
    payload: IncomingEmailPayload,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    x_zapier_secret: Optional[str] = Header(None, alias="X-Zapier-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
    token: Optional[str] = Query(None),
):
    """Webhook endpoint accepting parsed incoming emails from Zapier.

    - Validates shared webhook secret.
    - Captures sender, recipient, subject, body, timestamp, and attachment metadata.
    - Associates email with beneficiary application ID when available.
    - Deduplicates using message ID to prevent duplicate processing.
    - Logs safely without exposing sensitive patient/email text.

    This is deliberately a synchronous route: FastAPI runs it in its worker
    threadpool. Blocking provider/SMTP calls must not occupy the event loop,
    because vision providers fetch document images from this same server.
    """
    # 1. Validate Webhook Secret
    provided_secret = _extract_provided_secret(
        request=request,
        payload_secret=payload.webhook_secret,
        header_secret=x_webhook_secret,
        zapier_secret=x_zapier_secret,
        auth_header=authorization,
        query_secret=secret,
        query_token=token,
    )

    if not verify_webhook_secret(provided_secret):
        logger.warning(
            "Unauthorized incoming email webhook attempt from IP=%s",
            request.client.host if request.client else "unknown",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing webhook secret.",
        )

    # When the direct mailbox reader is enabled, do not let a text-only Zapier
    # event win the race and send a "missing files" reply before IMAP downloads
    # the actual MIME attachments. IMAP posts locally after saving those files.
    from_mailbox = request.client is not None and request.client.host in {"127.0.0.1", "::1"}
    documents_available = any(
        str(doc.get("url") or "").startswith(("https://", "http://")) or doc.get("extracted_text")
        for doc in attachment_service.normalize(payload.attachment_metadata)
    )
    if imap_service.imap_configured() and not from_mailbox and not documents_available:
        queued = db.execute(select(IncomingEmail).where(IncomingEmail.message_id == payload.message_id)).scalar_one_or_none()
        if queued is None:
            queued = IncomingEmail(
                message_id=payload.message_id, sender=payload.sender, recipient=payload.recipient,
                subject=payload.subject, body_plain=payload.body_plain, body_html=payload.body_html,
                attachment_count=0, received_at=payload.received_at or datetime.now(timezone.utc),
                raw_payload={'intake_status': 'awaiting_mailbox'},
            )
            db.add(queued)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()  # A concurrent full mailbox delivery already stored it.
        response.status_code = status.HTTP_202_ACCEPTED
        logger.info("Deferring text-only email webhook to the configured mailbox reader")
        return IncomingEmailResponse(
            status="awaiting_mailbox", message_id=payload.message_id,
            message="Awaiting the full mailbox delivery before document analysis. No review or reply has been generated.",
        )

    # 2. Check for Duplicate Message ID
    try:
        existing = db.execute(
            select(IncomingEmail).where(IncomingEmail.message_id == payload.message_id)
        ).scalar_one_or_none()
    except SQLAlchemyError:
        db.rollback()
        logger.error(
            "Database error checking existing message_id=%s",
            _mask_identifier(payload.message_id),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error. Please try again.",
        )

    resume_from_mailbox = False
    if existing is not None and isinstance(existing.raw_payload, dict) and (existing.raw_payload.get('intake_status') == 'review_pending' or (existing.raw_payload.get('intake_status') == 'awaiting_mailbox' and from_mailbox)):
        existing = db.execute(select(IncomingEmail).where(IncomingEmail.id == existing.id)
                              .with_for_update().execution_options(populate_existing=True)).scalar_one()
        resume_from_mailbox = (existing.raw_payload or {}).get('intake_status') in {'awaiting_mailbox', 'review_pending'}
    if existing is not None and not resume_from_mailbox:
        documents = attachment_service.merge(existing.attachment_metadata, payload.attachment_metadata)
        documents = attachment_service.merge(documents, attachment_service.stored_metadata(db, [payload.message_id]).get(payload.message_id, []))
        existing.attachment_metadata = documents or None
        existing.attachment_count = len(documents)
        db.commit()
        logger.info(
            "Duplicate incoming email skipped: message_id=%s, existing_id=%s, app_id=%s",
            _mask_identifier(payload.message_id),
            existing.id,
            existing.application_id,
        )
        # 200 OK prevents Zapier from retrying indefinitely
        response.status_code = status.HTTP_200_OK
        return IncomingEmailResponse(
            status="already_processed",
            email_id=str(existing.id),
            message_id=existing.message_id,
            application_id=existing.application_id,
            case_id=str(existing.case_id) if existing.case_id else None,
            duplicate=True,
            message="Email with this message ID was already processed.",
        )

    # 3. Format and normalize attachment metadata as a clean list of {filename, url} (+ optional content_type/size)
    raw_attachments = attachment_service.merge(
        payload.attachment_metadata,
        attachment_service.stored_metadata(db, [payload.message_id]).get(payload.message_id, []),
    )
    serialized_attachments: list[dict[str, Any]] = []
    for idx, att in enumerate(raw_attachments):
        raw_dict = att.model_dump(exclude_none=True) if hasattr(att, "model_dump") else (att if isinstance(att, dict) else {"url": str(att)})
        url_val = (
            raw_dict.get("url")
            or raw_dict.get("attachment_url")
            or raw_dict.get("file_url")
            or raw_dict.get("file")
        )
        fname_val = (
            raw_dict.get("filename")
            or raw_dict.get("name")
            or (
                f"Attached Document #{idx + 1}"
                if str(url_val).strip() == "<A File Object>"
                else (str(url_val).split("/")[-1] if url_val else f"document_{idx + 1}")
            )
        )
        if str(fname_val).strip() == "<A File Object>":
            fname_val = f"Attached Document #{idx + 1}"
        clean_doc: dict[str, Any] = {
            "filename": str(fname_val),
            "url": str(url_val) if url_val else None,
        }
        if raw_dict.get("content_type"):
            clean_doc["content_type"] = raw_dict["content_type"]
        if raw_dict.get("size") is not None:
            clean_doc["size"] = raw_dict["size"]
        if raw_dict.get("extracted_text"):
            clean_doc["extracted_text"] = str(raw_dict["extracted_text"])[:3000]
        serialized_attachments.append(clean_doc)

    # 4. Normalize received_at timestamp
    received_timestamp = payload.received_at or datetime.now(timezone.utc)
    if received_timestamp.tzinfo is None:
        received_timestamp = received_timestamp.replace(tzinfo=timezone.utc)

    # 5. Prepare audit raw payload (stripping webhook secret)
    raw_body_dict: dict[str, Any] = {}
    try:
        raw_body_dict = payload.model_dump(exclude={"webhook_secret"}, mode="json")
    except Exception:
        pass

    raw_body_dict['intake_status'] = 'processed'

    # 6. Auto-resolve linked Case if possible
    matched_case = _resolve_case(
        db=db,
        case_ref=payload.case_id,
        app_id=payload.application_id,
        sender_email=payload.sender,
        thread_references=re.findall(r'<[^<>]+>|[^\s,]+', ' '.join(filter(None, [payload.in_reply_to, payload.references]))),
    )

    if matched_case is None and resume_from_mailbox and existing.case_id:
        matched_case = db.get(Case, existing.case_id)

    if matched_case is None:
        candidate_case_num = (payload.application_id.strip()
                              if payload.application_id and len(payload.application_id.strip()) <= 32
                              else f"CASE-{datetime.now().year}-{secrets.token_hex(3).upper()}")
        if db.execute(select(Case.id).where(Case.case_number == candidate_case_num)).first():
            candidate_case_num = f"{candidate_case_num[:26]}-{secrets.token_hex(2).upper()}"
        matched_case = Case(case_number=candidate_case_num,
                            patient_email=ai_service._extract_email_address(payload.sender),
                            status='under_review', currency='USD', urgency='medium',
                            next_action='Review the incoming email and supporting documents')
        db.add(matched_case)
        db.flush()

    # Register one document per attachment before analysis. The same email and
    # document IDs are retained when the review result is saved below.
    prepared_email = existing if resume_from_mailbox else IncomingEmail(
        message_id=payload.message_id, sender=payload.sender, recipient=payload.recipient,
        subject=payload.subject, body_plain=payload.body_plain, body_html=payload.body_html,
        received_at=received_timestamp, attachment_metadata=serialized_attachments,
        attachment_count=len(serialized_attachments), raw_payload={'intake_status': 'review_pending'})
    prepared_email.case_id = matched_case.id if matched_case else None
    if matched_case and matched_case.status == 'approved' and matched_case.approval_source in {approval_policy.DOCUMENT_CHECKS, 'ai_red_flag_review'}:
        matched_case.status = 'under_review'
        matched_case.approval_source = None
        matched_case.next_action = 'Review the latest email and evidence before payment'
    db.add(prepared_email)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        duplicate = db.execute(select(IncomingEmail).where(IncomingEmail.message_id == payload.message_id)).scalar_one_or_none()
        if duplicate is None:
            raise
        response.status_code = status.HTTP_200_OK
        return IncomingEmailResponse(status='already_received', message_id=payload.message_id,
                                     email_id=str(duplicate.id), duplicate=True,
                                     message='The email has already been received; its review is pending or complete.')
    document_records = document_review_store.register_documents(db, prepared_email, serialized_attachments)
    serialized_attachments = [{**attachment, 'document_id': str(document.id)}
                              for attachment, document in zip(serialized_attachments, document_records)]
    for document, attachment in zip(document_records, serialized_attachments):
        document.source_id = str(document.id)
        document.file_metadata = attachment
    prepared_email.attachment_metadata = serialized_attachments or None

    db.commit()  # Files and their source email survive a provider/server failure.

    existing_context: Optional[dict[str, Any]] = None
    if matched_case:
        matched_case = db.execute(select(Case).where(Case.id == matched_case.id)
                                  .with_for_update().execution_options(populate_existing=True)).scalar_one()
        if matched_case.status == 'approved' and matched_case.approval_source in {approval_policy.DOCUMENT_CHECKS, 'ai_red_flag_review'}:
            matched_case.status = 'under_review'
            matched_case.approval_source = None
            matched_case.next_action = 'Review the latest email and evidence before payment'
        document_review_store.backfill_case(db, matched_case)
        existing_context = {
            **document_review_store.context(db, matched_case, prepared_email.id),
            "case_number": matched_case.case_number,
            "patient_name": matched_case.patient_name,
            "patient_email": matched_case.patient_email,
            "paypal_email": matched_case.paypal_email,
            "verification_evidence": matched_case.verification_evidence,
            "verification_issues": matched_case.verification_issues,
            "review_report": matched_case.review_report,
            "medical_category": matched_case.medical_category,
            "hospital_name": matched_case.hospital_name,
            "estimated_cost": str(matched_case.estimated_cost) if matched_case.estimated_cost else None,
            "requested_amount": str(matched_case.requested_amount) if matched_case.requested_amount else None,
            "urgency": matched_case.urgency,
            "status": matched_case.status,
            "overall_summary": matched_case.overall_summary,
            "next_action": matched_case.next_action,
            "pending_items": matched_case.pending_items,
        }

    # 7. Run AI triage & living summary analysis (via OpenRouter with safe fallback)
    ai_result = payload.ai_summary
    if not ai_result:
        ai_result = ai_service.analyze_incoming_email(
            sender=payload.sender,
            subject=payload.subject,
            body_plain=payload.body_plain,
            attachment_metadata=serialized_attachments,
            existing_case_context=existing_context,
        )

    analysis_failed = isinstance(ai_result, dict) and ai_result.get('analysis_status') == 'failed'
    if isinstance(ai_result, dict) and not analysis_failed:
        if matched_case and matched_case.requested_amount is not None:
            ai_result['requested_amount'] = str(matched_case.requested_amount)
        ai_result = approval_policy.constrain_email_analysis(
            ai_result, payload.sender, payload.subject, payload.body_plain, serialized_attachments,
            existing_evidence=matched_case.verification_evidence if matched_case else None,
            existing_issues=matched_case.verification_issues if matched_case else None,
            existing_report=matched_case.review_report if matched_case else None,
        )

    if matched_case and matched_case.status in {'rejected', 'closed'} and isinstance(ai_result, dict) and not analysis_failed:
        ai_result['status'] = matched_case.status
        ai_result['is_100_percent_verified'] = False
        ai_result['approval_source'] = None
        ai_result['auto_reply_body'] = (
            f'Your case remains {matched_case.status}. Please contact the Hope team if you would like to request a further review.'
        )

    # Existing approvals have no trustworthy provenance after the old AI flag
    # path. Preserve completed/in-flight payouts, but require review before a
    # legacy approved case can create a new payout.
    if (matched_case and matched_case.status == 'approved'
            and matched_case.approval_source not in approval_policy.TRUSTED_APPROVALS
            and isinstance(ai_result, dict) and not analysis_failed and not ai_result.get('is_100_percent_verified')):
        matched_case.status = 'under_review'
        matched_case.approval_source = None
        if isinstance(ai_result, dict):
            ai_result['status'] = 'under_review'
            ai_result['auto_reply_body'] = approval_policy.REVIEW_MESSAGE
            ai_result['next_action'] = 'Review previous unsupported approval before authorizing payment'

    # 8. Create or update the linked Case record with AI living summary
    if isinstance(ai_result, dict):
        est_cost = ai_service.to_decimal_or_none(ai_result.get("estimated_cost"))
        req_amt = ai_service.to_decimal_or_none(ai_result.get("requested_amount"))
        if not analysis_failed:
            if ai_result.get("overall_summary"):
                matched_case.overall_summary = str(ai_result["overall_summary"])
            if ai_result.get("next_action"):
                matched_case.next_action = str(ai_result["next_action"])[:255]
            if ai_result.get("pending_items") is not None:
                matched_case.pending_items = ai_result["pending_items"]
            if not matched_case.patient_name and ai_result.get("patient_name"):
                matched_case.patient_name = str(ai_result["patient_name"])[:255]
            if ai_result.get('medical_category'):
                matched_case.medical_category = str(ai_result['medical_category'])[:64]
            if ai_result.get('treatment_description'):
                matched_case.treatment_description = str(ai_result['treatment_description'])
            if ai_result.get('urgency'):
                matched_case.urgency = str(ai_result['urgency']).lower()[:32]
            if not matched_case.hospital_name and ai_result.get("hospital_name"):
                matched_case.hospital_name = str(ai_result["hospital_name"])[:255]
            if not matched_case.estimated_cost and est_cost is not None:
                matched_case.estimated_cost = est_cost
            if not matched_case.requested_amount and req_amt is not None:
                matched_case.requested_amount = req_amt
            matched_case.verification_evidence = ai_result.get('verification_evidence')
            matched_case.verification_issues = ai_result.get('verification_issues')
            matched_case.review_report = ai_result.get('review_report')
            if matched_case.status not in ('payout_processing', 'disbursed', 'paid') and matched_case.approval_source != approval_policy.REVIEWER:
                matched_case.status = str(ai_result['status'])
                matched_case.approval_source = ai_result.get('approval_source')


    if matched_case and analysis_failed:
        matched_case.next_action = str(ai_result['next_action'])
        pending = matched_case.pending_items if isinstance(matched_case.pending_items, list) else []
        matched_case.pending_items = list(dict.fromkeys([*map(str, pending), 'document_analysis_retry']))

    if matched_case and not matched_case.paypal_email and not analysis_failed:
        # Only payment details supplied by this case's contact can set the beneficiary.
        contact = ai_service._extract_email_address(payload.sender).lower()
        if contact == (matched_case.patient_email or "").lower():
            matched_case.paypal_email = case_workflow.extract_paypal_email(
                payload.body_plain,
                awaiting_email=(existing_context or {}).get('next_action') == 'Request beneficiary PayPal email',
            )

    resolved_app_id = payload.application_id or (matched_case.case_number if matched_case else None)

    if isinstance(ai_result, dict) and ai_result.get('review_report'):
        raw_body_dict['review_report'] = ai_result['review_report']

    # 9. Create database record (no per-email ai_summary; documents stored in attachment_metadata)
    email_values = dict(
        case_id=matched_case.id if matched_case else None,
        message_id=payload.message_id,
        sender=payload.sender,
        recipient=payload.recipient,
        subject=payload.subject,
        body_plain=payload.body_plain,
        body_html=payload.body_html,
        attachment_metadata=serialized_attachments if serialized_attachments else None,
        attachment_count=len(serialized_attachments),
        application_id=resolved_app_id,
        raw_payload=raw_body_dict if raw_body_dict else None,
        received_at=received_timestamp,
    )
    email_record = prepared_email
    for field, value in email_values.items():
        setattr(email_record, field, value)
    if matched_case and isinstance(ai_result, dict):
        snapshot = document_review_store.save_review(db, matched_case, email_record, document_records, ai_result)
        if (snapshot is not None and payload.ai_summary is None and ai_result.get('draft_required')
                and matched_case.status not in {'closed', 'rejected'}):
            ai_result['auto_reply_body'] = ai_service.draft_review_email(ai_result, matched_case.case_number)
            snapshot.reply_draft = ai_result['auto_reply_body']

    # 9b. Auto-generate & queue AI Reply email if payload did not explicitly disable auto-reply
    auto_reply_record: Optional[OutgoingEmail] = None
    if payload.ai_summary is None and isinstance(ai_result, dict) and ai_result.get("auto_reply_body"):
        reply_to_addr = ai_service._extract_email_address(payload.sender)
        if reply_to_addr and "@" in reply_to_addr:
            # Keep subject strictly as 'Re: <Original Subject>' so Gmail threads it into the same conversation
            reply_subj = ai_service._format_threaded_reply_subject(payload.subject)[:500]
            reply_body_str = str(ai_result["auto_reply_body"])
            if resolved_app_id and resolved_app_id not in reply_body_str:
                reply_body_str = reply_body_str.replace(
                    "--- CASE VERIFICATION STATUS ---\n",
                    f"--- CASE VERIFICATION STATUS ---\n• Case ID: {resolved_app_id}\n",
                    1,
                )
            auto_reply_record = OutgoingEmail(
                case_id=matched_case.id if matched_case else None,
                application_id=resolved_app_id or "GENERAL",
                recipient_email=reply_to_addr,
                subject=reply_subj,
                body_plain=reply_body_str,
                reply_to_message_id=payload.message_id,
                status="pending",
                raw_payload={"auto_generated_by_ai": not analysis_failed, "model": ai_result.get("model_used"),
                             "analysis_status": ai_result.get("analysis_status"),
                             "failure_reason": ai_result.get("failure_reason")},
            )

    try:
        db.add(email_record)
        if auto_reply_record is not None:
            db.add(auto_reply_record)
        db.flush()

        # 9c. Append ordered email primary keys to matched_case.email_exchanges
        if matched_case is not None:
            current_exchanges = list(matched_case.email_exchanges) if isinstance(matched_case.email_exchanges, list) else []
            current_exchanges.append({"id": str(email_record.id), "direction": "incoming"})
            if auto_reply_record is not None:
                current_exchanges.append({"id": str(auto_reply_record.id), "direction": "outgoing"})
            matched_case.email_exchanges = current_exchanges

        db.commit()
        db.refresh(email_record)
        if auto_reply_record is not None:
            db.refresh(auto_reply_record)
    except IntegrityError:
        # Concurrent request already inserted this message_id: return the existing record
        db.rollback()
        existing_row = db.execute(
            select(IncomingEmail).where(IncomingEmail.message_id == payload.message_id)
        ).scalar_one_or_none()
        if existing_row is not None:
            logger.info(
                "Concurrent duplicate incoming email caught: message_id=%s, existing_id=%s",
                _mask_identifier(payload.message_id),
                existing_row.id,
            )
            response.status_code = status.HTTP_200_OK
            return IncomingEmailResponse(
                status="already_processed",
                email_id=str(existing_row.id),
                message_id=existing_row.message_id,
                application_id=existing_row.application_id,
                case_id=str(existing_row.case_id) if existing_row.case_id else None,
                duplicate=True,
                message="Email with this message ID was already processed.",
            )
        logger.error("Integrity error on incoming email: message_id=%s", _mask_identifier(payload.message_id))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database integrity error occurred.",
        )
    except SQLAlchemyError:
        db.rollback()
        logger.exception(
            "Database error storing incoming email: message_id=%s",
            _mask_identifier(payload.message_id),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while storing incoming email.",
        )

    # Safe logging with PII/PHI protected
    logger.info(
        "Incoming email stored successfully: email_id=%s, message_id=%s, sender=%s, attachments=%d, app_id=%s",
        email_record.id,
        _mask_identifier(email_record.message_id),
        _mask_email(email_record.sender),
        email_record.attachment_count,
        email_record.application_id or "none",
    )

    if matched_case is not None and payload.ai_summary is None and not analysis_failed:
        payment_reply = case_workflow.process_approved_case(db, matched_case)
        if payment_reply and auto_reply_record is not None:
            name = matched_case.patient_name or 'there'
            if matched_case.approval_source == 'ai_red_flag_review':
                auto_reply_record.body_plain = f"{auto_reply_record.body_plain}\n\nPayment update:\n{payment_reply}\n\nCase: {matched_case.case_number}"
            else:
                auto_reply_record.body_plain = f"Hi {name},\n\n{payment_reply}\n\nCase: {matched_case.case_number}\n\nWarm regards,\nHope Medical Team"
        db.commit()

    # 10a. Prefer direct SMTP (sets In-Reply-To/References so Gmail threads it as a reply)
    sent_via_smtp = False
    if auto_reply_record is not None and smtp_service.smtp_configured():
        sent_via_smtp = smtp_service.send_threaded_email(
            to_addr=auto_reply_record.recipient_email,
            subject=auto_reply_record.subject,
            body=auto_reply_record.body_plain or "",
            in_reply_to=auto_reply_record.reply_to_message_id,
        )
        if sent_via_smtp:
            try:
                auto_reply_record.status = "sent"
                db.commit()
            except SQLAlchemyError:
                db.rollback()

    # 10b. Otherwise fall back to the Zapier Catch Hook
    zapier_hook = os.getenv("ZAPIER_OUTBOUND_WEBHOOK_URL") or DEFAULT_ZAPIER_OUTBOUND_HOOK
    if auto_reply_record is not None and zapier_hook and not sent_via_smtp:
        try:
            requests.post(
                zapier_hook.strip(),
                json={
                    "email_id": str(auto_reply_record.id),
                    "application_id": auto_reply_record.application_id,
                    "to": auto_reply_record.recipient_email,
                    "recipient_email": auto_reply_record.recipient_email,
                    "subject": auto_reply_record.subject,
                    "body": auto_reply_record.body_plain,
                    "reply_to_message_id": auto_reply_record.reply_to_message_id,
                    "in_reply_to": auto_reply_record.reply_to_message_id,
                    "references": auto_reply_record.reply_to_message_id,
                },
                timeout=5,
            )
        except Exception as exc:
            logger.warning("Failed to trigger Zapier outbound webhook for auto-reply: %s", exc)

    return IncomingEmailResponse(
        status="received",
        email_id=str(email_record.id),
        message_id=email_record.message_id,
        application_id=email_record.application_id,
        case_id=str(email_record.case_id) if email_record.case_id else None,
        duplicate=False,
        message="Email webhook processed and stored successfully.",
        outgoing_email_id=str(auto_reply_record.id) if auto_reply_record else None,
        auto_reply_recipient=auto_reply_record.recipient_email if auto_reply_record else None,
        auto_reply_subject=auto_reply_record.subject if auto_reply_record else None,
        auto_reply_body=auto_reply_record.body_plain if auto_reply_record else None,
    )


@router.get(
    "/attachments/{attachment_id}",
    summary="Download an email attachment (unguessable UUID acts as the access token)",
)
def download_attachment(attachment_id: str, db: Session = Depends(get_db)):
    try:
        att_uuid = uuid.UUID(attachment_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Attachment not found.")
    record = db.get(EmailAttachment, att_uuid)
    if record is None:
        raise HTTPException(status_code=404, detail="Attachment not found.")
    safe_name = (record.filename or "attachment").replace('"', "")
    return Response(
        content=record.data,
        media_type=record.content_type or "application/octet-stream",
        headers={"Content-Disposition": f'inline; filename="{safe_name}"'},
    )


@router.get(
    "/incoming",
    response_model=list[IncomingEmailListItem],
    summary="List stored incoming emails with optional filtering",
)
async def list_incoming_emails(
    request: Request,
    case_id: Optional[str] = Query(None, description="Filter by Case UUID or case_number"),
    application_id: Optional[str] = Query(None),
    sender: Optional[str] = Query(None),
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    if not _authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing webhook secret.",
        )

    stmt = select(IncomingEmail).order_by(IncomingEmail.received_at.desc())
    if case_id:
        matched = _resolve_case(db=db, case_ref=case_id)
        if matched:
            stmt = stmt.where(IncomingEmail.case_id == matched.id)
        else:
            return []
    if application_id:
        stmt = stmt.where(IncomingEmail.application_id == application_id.strip())
    if sender:
        stmt = stmt.where(IncomingEmail.sender == sender.strip())

    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    saved_files = attachment_service.stored_metadata(db, [row.message_id for row in rows])
    resolved_files = {row.id: attachment_service.merge(row.attachment_metadata, saved_files.get(row.message_id, [])) for row in rows}
    return [
        IncomingEmailListItem(
            review_report=(r.raw_payload or {}).get('review_report'),
            id=str(r.id),
            case_id=str(r.case_id) if r.case_id else None,
            message_id=r.message_id,
            sender=r.sender,
            recipient=r.recipient,
            subject=r.subject,
            body_plain=r.body_plain,
            body_html=r.body_html,
            attachment_metadata=resolved_files[r.id],
            attachment_count=len(resolved_files[r.id]),
            application_id=r.application_id,
            received_at=r.received_at,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in rows
    ]


@router.patch(
    "/incoming/{email_id}",
    response_model=IncomingEmailListItem,
    summary="Update case linkage or attachment metadata for an incoming email",
)
async def update_incoming_email(
    email_id: str,
    payload: UpdateIncomingEmailPayload,
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    if not _authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing webhook secret.",
        )

    try:
        val_uuid = uuid.UUID(email_id.strip())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email_id format, must be UUID.",
        )

    record = db.execute(select(IncomingEmail).where(IncomingEmail.id == val_uuid)).scalar_one_or_none()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incoming email record not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)
    if "case_id" in update_data and update_data["case_id"]:
        matched = _resolve_case(db=db, case_ref=update_data["case_id"])
        if not matched:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referenced case not found.")
        record.case_id = matched.id
    if "application_id" in update_data:
        record.application_id = update_data["application_id"]
    if "attachment_metadata" in update_data and update_data["attachment_metadata"] is not None:
        record.attachment_metadata = update_data["attachment_metadata"]
        record.attachment_count = len(update_data["attachment_metadata"])

    db.commit()
    db.refresh(record)

    return IncomingEmailListItem(
        review_report=(record.raw_payload or {}).get('review_report'),
        id=str(record.id),
        case_id=str(record.case_id) if record.case_id else None,
        message_id=record.message_id,
        sender=record.sender,
        recipient=record.recipient,
        subject=record.subject,
        body_plain=record.body_plain,
        body_html=record.body_html,
        attachment_metadata=record.attachment_metadata,
        attachment_count=record.attachment_count,
        application_id=record.application_id,
        received_at=record.received_at,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


@router.post(
    "/send",
    response_model=OutgoingEmailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Queue an outbound hospital verification email for Zapier/Hostinger dispatch",
)
async def send_outbound_email(
    payload: OutgoingEmailPayload,
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    x_zapier_secret: Optional[str] = Header(None, alias="X-Zapier-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
    token: Optional[str] = Query(None),
):
    """Queue an outbound verification email into PostgreSQL.

    - Authenticates using shared webhook secret or internal token.
    - Captures application_id, recipient_email, subject, body, and correlation info.
    - Stores record with status='pending' and returns email ID.
    - Does NOT send SMTP directly; Zapier detects and dispatches via Hostinger.
    - Protects privacy by masking identifiers and never logging email body content.
    """
    if not _authenticate_request(
        request=request,
        payload_secret=payload.webhook_secret,
        header_secret=x_webhook_secret,
        zapier_secret=x_zapier_secret,
        auth_header=authorization,
        query_secret=secret,
        query_token=token,
    ):
        logger.warning(
            "Unauthorized outbound email queue attempt from IP=%s",
            request.client.host if request.client else "unknown",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing webhook secret.",
        )

    # Basic email format validation
    recipient = payload.recipient_email.strip()
    if "@" not in recipient or "." not in recipient.split("@")[-1]:
        raise HTTPException(
            status_code=getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422),
            detail="Invalid recipient email address format.",
        )

    # Sanitize payload for raw storage (exclude secret)
    raw_payload_dict: dict[str, Any] = {}
    try:
        raw_payload_dict = payload.model_dump(exclude={"webhook_secret"}, mode="json")
    except Exception:
        pass

    matched_case = _resolve_case(
        db=db,
        case_ref=payload.case_id,
        app_id=payload.application_id,
    )
    resolved_app_id = (
        matched_case.case_number
        if matched_case and (not payload.application_id or payload.application_id == "GENERAL")
        else (payload.application_id or "GENERAL").strip()
    )

    outgoing_record = OutgoingEmail(
        case_id=matched_case.id if matched_case else None,
        application_id=resolved_app_id,
        recipient_email=recipient,
        subject=payload.subject.strip(),
        body_plain=payload.body,
        body_html=payload.body_html,
        reply_to_message_id=payload.reply_to_message_id.strip() if payload.reply_to_message_id else None,
        correlation_id=payload.correlation_id.strip() if payload.correlation_id else None,
        status="pending",
        raw_payload=raw_payload_dict if raw_payload_dict else None,
    )

    try:
        db.add(outgoing_record)
        db.flush()
        if matched_case is not None:
            current_exchanges = list(matched_case.email_exchanges) if isinstance(matched_case.email_exchanges, list) else []
            current_exchanges.append({"id": str(outgoing_record.id), "direction": "outgoing"})
            matched_case.email_exchanges = current_exchanges
        db.commit()
        db.refresh(outgoing_record)
    except SQLAlchemyError:
        db.rollback()
        logger.exception(
            "Database error queueing outbound email: app_id=%s",
            _mask_identifier(payload.application_id),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while queueing outbound email.",
        )

    # Privacy-safe logging (never logs email body or medical details)
    logger.info(
        "Outbound email queued successfully: email_id=%s, app_id=%s, recipient=%s, reply_to=%s, status=pending",
        outgoing_record.id,
        _mask_identifier(outgoing_record.application_id),
        _mask_email(outgoing_record.recipient_email),
        _mask_identifier(outgoing_record.reply_to_message_id),
    )

    # If Zapier outbound webhook is configured, notify it immediately for instant sending
    zapier_hook = os.getenv("ZAPIER_OUTBOUND_WEBHOOK_URL") or DEFAULT_ZAPIER_OUTBOUND_HOOK
    if zapier_hook:
        try:
            requests.post(
                zapier_hook.strip(),
                json={
                    "email_id": str(outgoing_record.id),
                    "application_id": outgoing_record.application_id,
                    "to": outgoing_record.recipient_email,
                    "recipient_email": outgoing_record.recipient_email,
                    "subject": outgoing_record.subject,
                    "body": outgoing_record.body_plain,
                    "reply_to_message_id": outgoing_record.reply_to_message_id,
                    "correlation_id": outgoing_record.correlation_id,
                },
                timeout=5,
            )
            logger.info("Outbound email forwarded to Zapier webhook: email_id=%s", outgoing_record.id)
        except Exception as exc:
            logger.warning("Failed to trigger Zapier outbound webhook: %s", exc)

    return OutgoingEmailResponse(
        status="pending",
        email_id=str(outgoing_record.id),
        application_id=outgoing_record.application_id,
        case_id=str(outgoing_record.case_id) if outgoing_record.case_id else None,
        recipient_email=outgoing_record.recipient_email,
        subject=outgoing_record.subject,
        reply_to_message_id=outgoing_record.reply_to_message_id,
        correlation_id=outgoing_record.correlation_id,
        created_at=outgoing_record.created_at,
        message="Outbound verification email queued successfully. Pending dispatch via Hostinger/Zapier.",
    )


@router.get(
    "/outgoing",
    response_model=list[OutgoingEmailListItem],
    summary="List all outbound emails with optional filtering",
)
async def list_outgoing_emails(
    request: Request,
    status_filter: Optional[str] = Query(None, alias="status"),
    case_id: Optional[str] = Query(None),
    application_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    """Retrieve outbound emails (pending, sent, failed) for dashboard and audit views."""
    if not _authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing webhook secret.",
        )

    stmt = select(OutgoingEmail).order_by(OutgoingEmail.created_at.desc())
    if status_filter:
        stmt = stmt.where(OutgoingEmail.status == status_filter.strip().lower())
    if case_id:
        matched = _resolve_case(db=db, case_ref=case_id)
        if matched:
            stmt = stmt.where(OutgoingEmail.case_id == matched.id)
        else:
            return []
    if application_id:
        stmt = stmt.where(OutgoingEmail.application_id == application_id.strip())

    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    return [
        OutgoingEmailListItem(
            id=str(r.id),
            case_id=str(r.case_id) if r.case_id else None,
            application_id=r.application_id,
            recipient_email=r.recipient_email,
            subject=r.subject,
            body_plain=r.body_plain,
            body_html=r.body_html,
            reply_to_message_id=r.reply_to_message_id,
            correlation_id=r.correlation_id,
            status=r.status,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in rows
    ]


@router.get(
    "/pending",
    response_model=list[OutgoingEmailListItem],
    summary="List pending outbound emails for Zapier/Hostinger polling",
)
async def list_pending_emails(
    request: Request,
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    """Retrieve queued outbound emails with status='pending' for Zapier to process."""
    if not _authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing webhook secret.",
        )

    rows = db.execute(
        select(OutgoingEmail)
        .where(OutgoingEmail.status == "pending")
        .order_by(OutgoingEmail.created_at.asc())
        .limit(limit)
    ).scalars().all()

    return [
        OutgoingEmailListItem(
            id=str(r.id),
            case_id=str(r.case_id) if r.case_id else None,
            application_id=r.application_id,
            recipient_email=r.recipient_email,
            subject=r.subject,
            body_plain=r.body_plain,
            body_html=r.body_html,
            reply_to_message_id=r.reply_to_message_id,
            correlation_id=r.correlation_id,
            status=r.status,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in rows
    ]


@router.post(
    "/dispatch-pending",
    summary="Push pending outbound emails to Zapier Catch Hook",
)
async def dispatch_pending_emails(
    request: Request,
    target_webhook_url: Optional[str] = Query(None, description="Optional Zapier Catch Hook URL override"),
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    """Triggers Zapier for all currently pending emails in the queue."""
    if not _authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing webhook secret.",
        )

    use_smtp = smtp_service.smtp_configured() and not target_webhook_url
    zapier_hook = target_webhook_url or os.getenv("ZAPIER_OUTBOUND_WEBHOOK_URL") or DEFAULT_ZAPIER_OUTBOUND_HOOK
    if not use_smtp and not zapier_hook:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Neither SMTP nor ZAPIER_OUTBOUND_WEBHOOK_URL is configured, and target_webhook_url was not provided.",
        )

    pending_rows = db.execute(
        select(OutgoingEmail).where(OutgoingEmail.status == "pending").order_by(OutgoingEmail.created_at.asc())
    ).scalars().all()

    dispatched = 0
    for r in pending_rows:
        if use_smtp:
            # Direct SMTP with In-Reply-To/References so Gmail threads it under the original email
            ok = smtp_service.send_threaded_email(
                to_addr=r.recipient_email,
                subject=r.subject,
                body=r.body_plain or "",
                in_reply_to=r.reply_to_message_id,
            )
            if ok:
                r.status = "sent"
                dispatched += 1
            else:
                logger.warning("SMTP dispatch failed for email_id=%s", r.id)
            continue
        try:
            requests.post(
                zapier_hook.strip(),
                json={
                    "email_id": str(r.id),
                    "application_id": r.application_id,
                    "to": r.recipient_email,
                    "recipient_email": r.recipient_email,
                    "subject": r.subject,
                    "body": r.body_plain,
                    "reply_to_message_id": r.reply_to_message_id,
                    "in_reply_to": r.reply_to_message_id,
                    "references": r.reply_to_message_id,
                    "correlation_id": r.correlation_id,
                },
                timeout=5,
            )
            dispatched += 1
        except Exception as e:
            logger.warning("Failed to dispatch email_id=%s to Zapier: %s", r.id, e)

    if use_smtp:
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()

    channel = "SMTP (threaded replies)" if use_smtp else "Zapier"
    return {
        "status": "ok",
        "dispatched_count": dispatched,
        "total_pending": len(pending_rows),
        "message": f"Successfully sent {dispatched} of {len(pending_rows)} pending emails via {channel}.",
    }


@router.patch(
    "/{email_id}/status",
    response_model=OutgoingEmailListItem,
    summary="Update delivery status of an outbound email",
)
async def update_email_status(
    email_id: str,
    payload: UpdateOutgoingEmailStatusPayload,
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    """Update status of an outgoing email (e.g. sent, failed) after Zapier dispatches through Hostinger."""
    if not _authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing webhook secret.",
        )

    try:
        val_uuid = uuid.UUID(email_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email_id format, must be UUID.",
        )

    record = db.execute(
        select(OutgoingEmail).where(OutgoingEmail.id == val_uuid)
    ).scalar_one_or_none()

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Outgoing email record not found.",
        )

    record.status = payload.status.lower()
    if payload.error_message:
        record.error_message = payload.error_message
    if payload.sent_message_id:
        record.correlation_id = payload.sent_message_id
    if record.status == "sent":
        record.sent_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(record)

    logger.info(
        "Outbound email status updated: email_id=%s, new_status=%s",
        record.id,
        record.status,
    )

    return OutgoingEmailListItem(
        id=str(record.id),
        case_id=str(record.case_id) if record.case_id else None,
        application_id=record.application_id,
        recipient_email=record.recipient_email,
        subject=record.subject,
        body_plain=record.body_plain,
        body_html=record.body_html,
        reply_to_message_id=record.reply_to_message_id,
        correlation_id=record.correlation_id,
        status=record.status,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


@router.delete(
    "/clear",
    summary="Clear all incoming and outgoing emails from the database",
)
async def clear_all_emails(
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    """Delete all stored incoming and outgoing email records."""
    if not _authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing webhook secret.",
        )

    from sqlalchemy import delete

    inc_res = db.execute(delete(IncomingEmail))
    out_res = db.execute(delete(OutgoingEmail))
    case_res = db.execute(delete(Case))
    db.execute(delete(EmailAttachment))
    db.commit()

    # Also mark everything currently unread in the mailbox as read, so the IMAP poller
    # does not re-import old emails as brand-new ones after a clear.
    mailbox_marked = imap_service.mark_all_seen()

    return {
        "status": "cleared",
        "deleted_incoming": inc_res.rowcount or 0,
        "deleted_outgoing": out_res.rowcount or 0,
        "deleted_cases": case_res.rowcount or 0,
        "mailbox_marked_read": mailbox_marked,
        "message": "All incoming emails, outgoing emails, and cases have been cleared.",
    }

