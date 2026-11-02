import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Any, Optional

SESSION_SECRET = os.getenv("SESSION_SECRET", "hope-admin-insecure-dev-session-secret-change-me")
SESSION_COOKIE_NAME = "hope_admin_session"
STATE_COOKIE_NAME = "hope_oauth_state"
SESSION_DURATION_SECONDS = 86400 * 7  # 7 days
STATE_DURATION_SECONDS = 600  # 10 minutes


def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64_decode(data: str) -> bytes:
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(message: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).digest()
    return _b64_encode(sig)


def generate_csrf_state() -> str:
    """Generate a high-entropy random state for OAuth CSRF protection."""
    random_part = secrets.token_urlsafe(32)
    timestamp = str(int(time.time()))
    payload = f"{random_part}:{timestamp}".encode("utf-8")
    sig = _sign(payload, SESSION_SECRET)
    return f"{_b64_encode(payload)}.{sig}"


def verify_csrf_state(state: str) -> bool:
    """Verify that state parameter is authentic and not expired."""
    try:
        parts = state.split(".")
        if len(parts) != 2:
            return False
        payload_b64, sig = parts
        payload = _b64_decode(payload_b64)
        expected_sig = _sign(payload, SESSION_SECRET)
        if not hmac.compare_digest(sig, expected_sig):
            return False

        # Check timestamp
        _, ts_str = payload.decode("utf-8").split(":", 1)
        created_at = int(ts_str)
        if time.time() - created_at > STATE_DURATION_SECONDS:
            return False
        return True
    except Exception:
        return False


def create_session_token(merchant_id: str, email: Optional[str] = None, name: Optional[str] = None) -> str:
    """Create a cryptographically signed session token containing merchant identity."""
    payload: dict[str, Any] = {
        "sub": merchant_id,
        "email": email,
        "name": name,
        "iat": int(time.time()),
        "exp": int(time.time()) + SESSION_DURATION_SECONDS,
    }
    raw_json = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    encoded_payload = _b64_encode(raw_json)
    signature = _sign(encoded_payload.encode("utf-8"), SESSION_SECRET)
    return f"{encoded_payload}.{signature}"


def verify_session_token(token: str) -> Optional[dict[str, Any]]:
    """Verify token signature and expiration. Returns payload dict or None."""
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        encoded_payload, signature = parts
        expected_sig = _sign(encoded_payload.encode("utf-8"), SESSION_SECRET)
        if not hmac.compare_digest(signature, expected_sig):
            return None

        raw_json = _b64_decode(encoded_payload)
        payload = json.loads(raw_json.decode("utf-8"))
        if time.time() > payload.get("exp", 0):
            return None
        return payload
    except Exception:
        return None
