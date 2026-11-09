"""Direct SMTP sender that sets In-Reply-To / References headers so replies thread in Gmail."""
import logging
import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from typing import Optional

logger = logging.getLogger(__name__)


def smtp_configured() -> bool:
    return bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_USER") and os.getenv("SMTP_PASSWORD"))


def send_threaded_email(
    to_addr: str,
    subject: str,
    body: str,
    in_reply_to: Optional[str] = None,
) -> bool:
    """Send a plain-text email; returns True on success. Never raises."""
    if not smtp_configured():
        return False

    host = os.environ["SMTP_HOST"].strip()
    port = int(os.getenv("SMTP_PORT", "465"))
    user = os.environ["SMTP_USER"].strip()
    password = os.environ["SMTP_PASSWORD"]
    from_addr = (os.getenv("SMTP_FROM") or user).strip()
    from_name = os.getenv("SMTP_FROM_NAME", "Hope Medical Verification Team").strip()

    msg = EmailMessage()
    msg["From"] = f"{from_name} <{from_addr}>"
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=from_addr.split("@")[-1])
    if in_reply_to:
        ref = in_reply_to.strip()
        if not ref.startswith("<"):
            ref = f"<{ref}>"
        msg["In-Reply-To"] = ref
        msg["References"] = ref
    msg.set_content(body)

    try:
        if port == 465:
            with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context(), timeout=20) as server:
                server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port, timeout=20) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(user, password)
                server.send_message(msg)
        logger.info("Threaded SMTP reply sent to %s", to_addr)
        return True
    except Exception as exc:
        logger.warning("SMTP send failed: %s", exc)
        return False

