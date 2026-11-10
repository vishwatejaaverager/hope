"""Background IMAP poller: reads the Hostinger mailbox directly, keeps real attachments, forwards to the incoming-email API."""
import email
import imaplib
import io
import logging
import os
import threading
import time
from datetime import timezone
from email import policy
from email.utils import parseaddr, parsedate_to_datetime
from typing import Any, Optional

import requests
from sqlalchemy import select

from app.db import SessionLocal
from app.models import EmailAttachment, IncomingEmail
from app.services import attachment_service

logger = logging.getLogger(__name__)

MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024
MAX_EXTRACTED_TEXT = 3000

_started = False


def imap_configured() -> bool:
    return bool(os.getenv("IMAP_HOST") and os.getenv("IMAP_USER") and os.getenv("IMAP_PASSWORD"))


def _extract_text(filename: str, content_type: str, data: bytes) -> Optional[str]:
    """Best-effort text extraction from PDFs and text files so the AI can read document contents."""
    name = (filename or "").lower()
    try:
        if name.endswith(".pdf") or content_type == "application/pdf":
            from pypdf import PdfReader  # optional dependency

            reader = PdfReader(io.BytesIO(data))
            text = "\n".join((page.extract_text() or "") for page in reader.pages[:10]).strip()
            return text[:MAX_EXTRACTED_TEXT] or None
        if content_type.startswith("text/") or name.endswith(".txt"):
            return data.decode("utf-8", errors="ignore").strip()[:MAX_EXTRACTED_TEXT] or None
    except Exception as exc:
        logger.warning("Text extraction failed for %s: %s", filename, exc)
    return None


def _base_url() -> str:
    return os.getenv("PUBLIC_BASE_URL", "https://hope-9dq5.onrender.com").rstrip("/")


def _process_message(raw: bytes) -> bool:
    """Parse one RFC822 message and post it to the incoming-email endpoint. Returns True on success."""
    msg = email.message_from_bytes(raw, policy=policy.default)
    message_id = (msg.get("Message-ID") or "").strip()
    if not message_id:
        return True  # nothing we can dedupe on; skip

    sender_addr = parseaddr(str(msg.get("From", "")))[1]
    own_addr = (os.getenv("IMAP_USER") or "").lower()
    if sender_addr.lower() == own_addr:
        return True  # never process our own outgoing mail

    with SessionLocal() as db:
        existing = db.execute(select(IncomingEmail).where(IncomingEmail.message_id == message_id)).scalar_one_or_none()
        saved_files = db.execute(select(EmailAttachment).where(EmailAttachment.message_id == message_id)).scalars().all()

        body_part = msg.get_body(preferencelist=("plain",))
        html_part = msg.get_body(preferencelist=("html",))
        body_plain = body_part.get_content() if body_part else None
        body_html = html_part.get_content() if html_part else None

        attachments: list[dict[str, Any]] = []
        for part in msg.iter_attachments():
            data = part.get_payload(decode=True) or b""
            filename = part.get_filename() or "attachment"
            if not data or len(data) > MAX_ATTACHMENT_BYTES:
                continue
            ctype = part.get_content_type()
            record = next((item for item in saved_files
                           if item.filename == filename and item.data == data), None)
            if record is None:
                record = EmailAttachment(
                    message_id=message_id, filename=filename, content_type=ctype,
                    size=len(data), data=data,
                )
                db.add(record)
                db.flush()
                saved_files.append(record)
            doc: dict[str, Any] = {
                "filename": filename,
                "url": f"{_base_url()}/api/v1/emails/attachments/{record.id}",
                "content_type": ctype,
                "size": len(data),
            }
            text = _extract_text(filename, ctype, data)
            if text:
                doc["extracted_text"] = text
            attachments.append(doc)
        if existing is not None:
            existing.attachment_metadata = attachment_service.merge(existing.attachment_metadata, attachments) or None
            existing.attachment_count = len(existing.attachment_metadata or [])
            waiting = isinstance(existing.raw_payload, dict) and existing.raw_payload.get('intake_status') == 'awaiting_mailbox'
            db.commit()
            if not waiting:
                return True  # Already reviewed; attach files without another reply or payout.
        db.commit()

    try:
        received = parsedate_to_datetime(str(msg.get("Date"))).astimezone(timezone.utc).isoformat()
    except Exception:
        received = None

    payload = {
        "message_id": message_id,
        "sender": sender_addr or str(msg.get("From", "")),
        "recipient": parseaddr(str(msg.get("To", "")))[1] or own_addr,
        "subject": str(msg.get("Subject", "")) or None,
        "body_plain": body_plain,
        "body_html": body_html,
        "received_at": received,
        "attachment_metadata": attachments or None,
    }
    port = os.getenv("PORT", "10000")
    resp = requests.post(
        f"http://127.0.0.1:{port}/api/v1/emails/incoming",
        json=payload,
        headers={"X-Webhook-Secret": os.getenv("EMAIL_WEBHOOK_SECRET", "")},
        timeout=90,
    )
    if not resp.ok:
        logger.warning("Incoming endpoint rejected IMAP email (%s): %s", resp.status_code, resp.text[:200])
    return resp.ok


def poll_once() -> int:
    host = os.environ["IMAP_HOST"].strip()
    port = int(os.getenv("IMAP_PORT", "993"))
    handled = 0
    with imaplib.IMAP4_SSL(host, port, timeout=20) as conn:
        conn.login(os.environ["IMAP_USER"].strip(), os.environ["IMAP_PASSWORD"])
        conn.select("INBOX")
        status, data = conn.search(None, "UNSEEN")
        if status != "OK":
            return 0
        message_numbers = list(data[0].split())
        # A Zapier/mail client may have marked the message read before this poll.
        # Recover only explicitly queued messages, not the entire historical inbox.
        with SessionLocal() as db:
            pending_ids = db.execute(
                select(IncomingEmail.message_id)
                .where(IncomingEmail.raw_payload['intake_status'].as_string() == 'awaiting_mailbox')
                .order_by(IncomingEmail.created_at).limit(25)
            ).scalars().all()
        for message_id in pending_ids:
            if any(character in message_id for character in ('\r', '\n', '"', '\\')):
                continue
            found_status, found = conn.search(None, 'HEADER', 'Message-ID', f'"{message_id}"')
            if found_status == 'OK' and found:
                for number in found[0].split():
                    if number not in message_numbers:
                        message_numbers.append(number)
        for num in message_numbers:
            status, fetched = conn.fetch(num, "(BODY.PEEK[])")
            if status != "OK" or not fetched or not isinstance(fetched[0], tuple):
                continue
            try:
                if _process_message(fetched[0][1]):
                    conn.store(num, "+FLAGS", "\\Seen")
                    handled += 1
            except Exception as exc:
                logger.exception("Failed processing IMAP message %s: %s", num, exc)
    return handled


def mark_all_seen() -> int:
    """Mark every unread message in the INBOX as read without processing it. Never raises."""
    if not imap_configured():
        return 0
    try:
        with imaplib.IMAP4_SSL(os.environ["IMAP_HOST"].strip(), int(os.getenv("IMAP_PORT", "993")), timeout=20) as conn:
            conn.login(os.environ["IMAP_USER"].strip(), os.environ["IMAP_PASSWORD"])
            conn.select("INBOX")
            status, data = conn.search(None, "UNSEEN")
            if status != "OK":
                return 0
            nums = data[0].split()
            for num in nums:
                conn.store(num, "+FLAGS", "\\Seen")
            return len(nums)
    except Exception as exc:
        logger.warning("Could not mark mailbox as read: %s", exc)
        return 0


def _loop() -> None:
    interval = int(os.getenv("IMAP_POLL_SECONDS", "30"))
    time.sleep(15)  # let the web server come up first
    while True:
        try:
            n = poll_once()
            if n:
                logger.info("IMAP poll processed %d new email(s)", n)
        except Exception as exc:
            logger.warning("IMAP poll failed: %s", exc)
        time.sleep(interval)


def start_poller() -> None:
    global _started
    if _started or not imap_configured():
        return
    _started = True
    threading.Thread(target=_loop, name="imap-poller", daemon=True).start()
    logger.info("IMAP poller started for %s", os.getenv("IMAP_USER"))

