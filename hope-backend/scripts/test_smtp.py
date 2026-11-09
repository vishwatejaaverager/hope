"""Check the SMTP login and send one threaded test email.

Usage (from hope-backend, with SMTP_* set in .env or the shell):
    .venv/bin/python scripts/test_smtp.py you@gmail.com
"""
import sys

from dotenv import load_dotenv

load_dotenv()

from app.services import smtp_service  # noqa: E402

if not smtp_service.smtp_configured():
    sys.exit("SMTP_HOST / SMTP_USER / SMTP_PASSWORD are not set.")

to = sys.argv[1] if len(sys.argv) > 1 else sys.exit("Pass a recipient address.")
ok = smtp_service.send_threaded_email(
    to_addr=to,
    subject="Re: SMTP threading test",
    body="If this arrived, Hostinger SMTP works.",
    in_reply_to="<test-thread@example.com>",
)
print("SENT" if ok else "FAILED (see the warning above for the reason)")

