import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import verify_session_token, verify_webhook_secret
from app.db import get_db
from app.models import IncomingEmail, OutgoingEmail
from app.schemas.email import (
    IncomingEmailPayload,
    IncomingEmailResponse,
    OutgoingEmailListItem,
    OutgoingEmailPayload,
    OutgoingEmailResponse,
    UpdateOutgoingEmailStatusPayload,
)

logger = logging.getLogger(__name__)

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
async def receive_incoming_email(
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

    if existing is not None:
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
            duplicate=True,
            message="Email with this message ID was already processed.",
        )

    # 3. Format and normalize attachment metadata
    raw_attachments = payload.attachment_metadata or []
    serialized_attachments: list[dict[str, Any]] = []
    for att in raw_attachments:
        if hasattr(att, "model_dump"):
            serialized_attachments.append(att.model_dump(exclude_none=True))
        elif isinstance(att, dict):
            serialized_attachments.append(att)
        else:
            serialized_attachments.append({"raw": str(att)})

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

    # 6. Create database record
    email_record = IncomingEmail(
        message_id=payload.message_id,
        sender=payload.sender,
        recipient=payload.recipient,
        subject=payload.subject,
        body_plain=payload.body_plain,
        body_html=payload.body_html,
        attachment_metadata=serialized_attachments if serialized_attachments else None,
        attachment_count=len(serialized_attachments),
        application_id=payload.application_id,
        raw_payload=raw_body_dict if raw_body_dict else None,
        received_at=received_timestamp,
    )

    try:
        db.add(email_record)
        db.commit()
        db.refresh(email_record)
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

    return IncomingEmailResponse(
        status="received",
        email_id=str(email_record.id),
        message_id=email_record.message_id,
        application_id=email_record.application_id,
        duplicate=False,
        message="Email webhook processed and stored successfully.",
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

    outgoing_record = OutgoingEmail(
        application_id=payload.application_id.strip(),
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

    return OutgoingEmailResponse(
        status="pending",
        email_id=str(outgoing_record.id),
        application_id=outgoing_record.application_id,
        recipient_email=outgoing_record.recipient_email,
        subject=outgoing_record.subject,
        reply_to_message_id=outgoing_record.reply_to_message_id,
        correlation_id=outgoing_record.correlation_id,
        created_at=outgoing_record.created_at,
        message="Outbound verification email queued successfully. Pending dispatch via Hostinger/Zapier.",
    )


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

