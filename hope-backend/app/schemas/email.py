import re
from datetime import datetime, timezone
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

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

        # 7. Normalize received_at / date
        if not data.get("received_at"):
            for alt in ("received_timestamp", "date", "timestamp", "Date"):
                if data.get(alt):
                    data["received_at"] = data[alt]
                    break

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
