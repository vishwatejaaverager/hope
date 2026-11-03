import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator


def parse_flexible_datetime(val: Any) -> Optional[datetime]:
    """Parse various email date formats (RFC 2822, ISO 8601, timestamps) into UTC datetime."""
    if not val:
        return None
    if isinstance(val, datetime):
        if val.tzinfo is None:
            return val.replace(tzinfo=timezone.utc)
        return val

    # If numeric timestamp
    if isinstance(val, (int, float)):
        try:
            return datetime.fromtimestamp(float(val), tz=timezone.utc)
        except Exception:
            pass

    if isinstance(val, str):
        val_str = val.strip()
        if not val_str:
            return None

        # Check if numeric string timestamp
        try:
            timestamp = float(val_str)
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        except ValueError:
            pass

        # 1. Try ISO 8601 (handling trailing 'Z' if present)
        try:
            iso_str = val_str
            if iso_str.endswith("Z"):
                iso_str = iso_str[:-1] + "+00:00"
            dt = datetime.fromisoformat(iso_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except (ValueError, TypeError):
            pass

        # 2. Try RFC 2822 email date format (e.g. "Tue, 03 Nov 2026 09:30:15 +0000")
        try:
            dt = parsedate_to_datetime(val_str)
            if dt is not None:
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
        except Exception:
            pass

        # 3. Try dateutil if available
        try:
            from dateutil import parser as dateutil_parser
            dt = dateutil_parser.parse(val_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            pass

    # Safe fallback: return current UTC timestamp so emails are never rejected
    return datetime.now(timezone.utc)

# Common patterns for beneficiary application IDs:
# e.g. APP-12345, APP_2026_001, BEN-9872, or UUID
APP_ID_PATTERNS = [
    re.compile(r"\b(APP[-_][A-Za-z0-9-_]{3,32})\b", re.IGNORECASE),
    re.compile(r"\b(BEN[-_][A-Za-z0-9-_]{3,32})\b", re.IGNORECASE),
    re.compile(r"(?:application|case)\s*(?:id|#|number)?\s*[:=\s]\s*([A-Za-z0-9-_]{4,36})", re.IGNORECASE),
    re.compile(r"\b([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\b"),
]


def extract_application_id(subject: Optional[str], body: Optional[str]) -> Optional[str]:
    """Inspect subject and body text to extract an application ID if present."""
    for text in (subject, body):
        if not text:
            continue
        for pattern in APP_ID_PATTERNS:
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
    return None


class AttachmentMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    filename: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    url: Optional[str] = None


class IncomingEmailPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    message_id: str = Field(..., description="Unique email message identifier")
    sender: str = Field(..., description="Sender email address")
    recipient: str = Field(..., description="Recipient email address")
    subject: Optional[str] = Field(None, max_length=500)
    body_plain: Optional[str] = None
    body_html: Optional[str] = None
    received_at: Optional[datetime] = None
    attachment_metadata: Optional[list[Union[AttachmentMetadata, dict[str, Any]]]] = None
    application_id: Optional[str] = Field(None, max_length=64)
    webhook_secret: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_zapier_fields(cls, values: Any) -> Any:
        if not isinstance(values, dict):
            return values

        data = dict(values)

        # 1. Normalize message_id
        if not data.get("message_id"):
            for alt in ("messageId", "message_ID", "id", "Message-ID", "email_id"):
                if data.get(alt):
                    data["message_id"] = str(data[alt]).strip()
                    break

        # 2. Normalize sender
        if not data.get("sender"):
            for alt in ("from", "from_email", "from_address", "sender_email", "From"):
                if data.get(alt):
                    data["sender"] = str(data[alt]).strip()
                    break

        # 3. Normalize recipient
        if not data.get("recipient"):
            for alt in ("to", "to_email", "to_address", "recipient_email", "To"):
                if data.get(alt):
                    data["recipient"] = str(data[alt]).strip()
                    break

        # 4. Normalize subject
        if not data.get("subject") and data.get("Subject"):
            data["subject"] = str(data["Subject"]).strip()

        # 5. Normalize body_plain
        if not data.get("body_plain"):
            for alt in ("body", "text", "body_text", "plain_text", "content"):
                if data.get(alt):
                    data["body_plain"] = str(data[alt])
                    break

        # 6. Normalize body_html
        if not data.get("body_html"):
            for alt in ("html", "body_html_content", "HTML"):
                if data.get(alt):
                    data["body_html"] = str(data[alt])
                    break

        # 7. Normalize and parse received_at / date
        raw_date = data.get("received_at")
        if not raw_date:
            for alt in ("received_timestamp", "date", "timestamp", "Date"):
                if data.get(alt):
                    raw_date = data[alt]
                    break
        data["received_at"] = parse_flexible_datetime(raw_date)

        # 8. Normalize attachment metadata
        if data.get("attachment_metadata") is None and data.get("attachments"):
            data["attachment_metadata"] = data.get("attachments")

        # 9. Extract or normalize application_id
        if not data.get("application_id"):
            for alt in ("applicationId", "case_id", "caseId"):
                if data.get(alt):
                    data["application_id"] = str(data[alt]).strip()
                    break

        if not data.get("application_id"):
            extracted = extract_application_id(data.get("subject"), data.get("body_plain"))
            if extracted:
                data["application_id"] = extracted

        # 10. Normalize webhook secret
        if not data.get("webhook_secret"):
            for alt in ("secret", "token"):
                if data.get(alt):
                    data["webhook_secret"] = str(data[alt]).strip()
                    break

        return data


class IncomingEmailResponse(BaseModel):
    status: str
    email_id: Optional[str] = None
    message_id: str
    application_id: Optional[str] = None
    duplicate: bool = False
    message: str


class OutgoingEmailPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    application_id: str = Field(..., description="Beneficiary or case application ID", max_length=64)
    recipient_email: str = Field(..., description="Recipient hospital or contact email address", max_length=255)
    subject: str = Field(..., description="Email subject", max_length=500)
    body: str = Field(..., description="Plain-text email body content")
    body_html: Optional[str] = Field(None, description="Optional HTML body content")
    reply_to_message_id: Optional[str] = Field(
        None, description="Optional email message ID this email is in reply to", max_length=255
    )
    correlation_id: Optional[str] = Field(
        None, description="Optional external tracking or correlation identifier", max_length=64
    )
    webhook_secret: Optional[str] = Field(None, description="Optional secret passed directly in JSON payload")

    @model_validator(mode="before")
    @classmethod
    def normalize_outbound_fields(cls, values: Any) -> Any:
        if not isinstance(values, dict):
            return values

        data = dict(values)

        # 1. Normalize application_id
        if not data.get("application_id"):
            for alt in ("applicationId", "case_id", "caseId", "app_id", "beneficiary_id"):
                if data.get(alt):
                    data["application_id"] = str(data[alt]).strip()
                    break

        # 2. Normalize recipient_email
        if not data.get("recipient_email"):
            for alt in ("to", "to_email", "to_address", "recipient", "email", "hospital_email"):
                if data.get(alt):
                    data["recipient_email"] = str(data[alt]).strip()
                    break

        # 3. Normalize subject
        if not data.get("subject") and data.get("Subject"):
            data["subject"] = str(data["Subject"]).strip()

        # 4. Normalize body
        if not data.get("body"):
            for alt in ("body_plain", "text", "body_text", "plain_text", "content", "message"):
                if data.get(alt):
                    data["body"] = str(data[alt])
                    break

        # 5. Normalize body_html
        if not data.get("body_html"):
            for alt in ("html", "body_html_content", "HTML"):
                if data.get(alt):
                    data["body_html"] = str(data[alt])
                    break

        # 6. Normalize reply_to_message_id
        if not data.get("reply_to_message_id"):
            for alt in ("reply_to", "in_reply_to", "in_reply_to_message_id", "message_id", "replyToMessageId"):
                if data.get(alt):
                    data["reply_to_message_id"] = str(data[alt]).strip()
                    break

        # 7. Normalize correlation_id
        if not data.get("correlation_id"):
            for alt in ("correlationId", "tracking_id", "reference_id"):
                if data.get(alt):
                    data["correlation_id"] = str(data[alt]).strip()
                    break

        # 8. Normalize webhook_secret
        if not data.get("webhook_secret"):
            for alt in ("secret", "token", "api_key", "key"):
                if data.get(alt):
                    data["webhook_secret"] = str(data[alt]).strip()
                    break

        return data


class OutgoingEmailResponse(BaseModel):
    status: str
    email_id: str
    application_id: str
    recipient_email: str
    subject: str
    reply_to_message_id: Optional[str] = None
    correlation_id: Optional[str] = None
    created_at: datetime
    message: str


class OutgoingEmailListItem(BaseModel):
    id: str
    application_id: str
    recipient_email: str
    subject: str
    body_plain: str
    body_html: Optional[str] = None
    reply_to_message_id: Optional[str] = None
    correlation_id: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


class UpdateOutgoingEmailStatusPayload(BaseModel):
    status: str = Field(..., description="New status, e.g. 'sent' or 'failed'")
    error_message: Optional[str] = Field(None, description="Optional error description if delivery failed")
    sent_message_id: Optional[str] = Field(None, description="Optional Message-ID assigned by mail server")

