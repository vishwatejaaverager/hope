import logging
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import verify_webhook_secret
from app.db import get_db
from app.models import IncomingEmail
from app.schemas.email import IncomingEmailPayload, IncomingEmailResponse

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
    payload_secret: Optional[str],
    header_secret: Optional[str],
    zapier_secret: Optional[str],
    auth_header: Optional[str],
    query_secret: Optional[str],
    query_token: Optional[str],
) -> Optional[str]:
    """Find the webhook secret in headers, query params, or payload body."""
    return (
        header_secret
        or zapier_secret
        or auth_header
        or query_secret
        or query_token
        or payload_secret
    )


@router.post(
    "/incoming",
    response_model=IncomingEmailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Receive incoming email webhook from Zapier",
)
async def receive_incoming_email(
    payload: IncomingEmailPayload,
    request: Request,
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
