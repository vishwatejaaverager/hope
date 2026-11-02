"""All PayPal REST API calls live here. Credentials come from environment only."""
import os
import time
import uuid

import requests
from dotenv import load_dotenv

load_dotenv()

PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL", "https://api-m.sandbox.paypal.com").rstrip("/")
CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

TIMEOUT = 30

# Simple in-process access token cache (tokens are valid ~9h).
_token_cache = {"token": None, "expires_at": 0.0}


class PayPalError(Exception):
    """Raised for any PayPal/network failure, with a safe message for clients."""

    def __init__(self, message: str, status_code: int = 502, name: str | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.name = name


def get_client_id() -> str:
    if not CLIENT_ID:
        raise PayPalError("PayPal client ID is not configured", 500)
    return CLIENT_ID


def _error_from_response(response: requests.Response) -> PayPalError:
    try:
        body = response.json()
    except ValueError:
        body = {}
    name = body.get("name")
    message = body.get("message") or "PayPal request failed"
    details = body.get("details") or []
    issues = [d.get("issue") for d in details if d.get("issue")]
    if issues:
        message = f"{message} ({', '.join(issues)})"
        name = issues[0]
    status = 502 if response.status_code >= 500 else (response.status_code if response.status_code in (400, 404, 422) else 502)
    return PayPalError(message, status, name)


def generate_access_token() -> str:
    if not CLIENT_ID or not CLIENT_SECRET:
        raise PayPalError("PayPal credentials are missing from .env", 500)

    if _token_cache["token"] and time.time() < _token_cache["expires_at"]:
        return _token_cache["token"]

    try:
        response = requests.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=(CLIENT_ID, CLIENT_SECRET),
            headers={"Accept": "application/json"},
            data={"grant_type": "client_credentials"},
            timeout=TIMEOUT,
        )
    except requests.RequestException:
        raise PayPalError("Could not reach PayPal. Please try again.", 502)

    if not response.ok:
        raise PayPalError("PayPal authentication failed", 502)

    data = response.json()
    _token_cache["token"] = data["access_token"]
    _token_cache["expires_at"] = time.time() + int(data.get("expires_in", 300)) - 60
    return _token_cache["token"]


def _request(method: str, path: str, **kwargs) -> requests.Response:
    token = generate_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        **kwargs.pop("headers", {}),
    }
    try:
        return requests.request(
            method, f"{PAYPAL_BASE_URL}{path}", headers=headers, timeout=TIMEOUT, **kwargs
        )
    except requests.RequestException:
        raise PayPalError("Could not reach PayPal. Please try again.", 502)


def create_order(amount: str, currency: str = "USD") -> dict:
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": f"HOPE-{uuid.uuid4().hex[:10]}",
                "description": "Hope Medical Fund Donation",
                "amount": {"currency_code": currency.upper(), "value": amount},
            }
        ],
    }
    response = _request(
        "POST",
        "/v2/checkout/orders",
        json=payload,
        headers={"PayPal-Request-Id": str(uuid.uuid4())},
    )
    if not response.ok:
        raise _error_from_response(response)
    return response.json()


def get_order(order_id: str) -> dict:
    response = _request("GET", f"/v2/checkout/orders/{order_id}")
    if not response.ok:
        raise _error_from_response(response)
    return response.json()


def capture_order(order_id: str) -> dict:
    """Capture an approved order. Safe against duplicate calls.

    A deterministic PayPal-Request-Id makes PayPal treat repeated captures of
    the same order as the same request. If PayPal still reports the order was
    already captured, we read the order's real state instead of retrying blindly.
    """
    response = _request(
        "POST",
        f"/v2/checkout/orders/{order_id}/capture",
        headers={"PayPal-Request-Id": f"hope-capture-{order_id}"},
    )
    if response.ok:
        return response.json()

    error = _error_from_response(response)
    if error.name == "ORDER_ALREADY_CAPTURED":
        return get_order(order_id)
    raise error


def create_payout(receiver_email: str, amount: str, note: str, currency: str = "USD") -> dict:
    """Send a single-item Payouts batch (Sandbox testing of merchant -> beneficiary)."""
    batch_id = f"HOPE-{uuid.uuid4().hex[:16]}"
    payload = {
        "sender_batch_header": {
            "sender_batch_id": batch_id,
            "email_subject": "You have a payout from Hope",
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "receiver": receiver_email,
                "amount": {"value": amount, "currency": currency.upper()},
                "note": note,
                "sender_item_id": f"{batch_id}-1",
            }
        ],
    }
    response = _request(
        "POST",
        "/v1/payments/payouts",
        json=payload,
        headers={"PayPal-Request-Id": batch_id},
    )
    if not response.ok:
        raise _error_from_response(response)
    return response.json()


def get_payout(batch_id: str) -> dict:
    response = _request("GET", f"/v1/payments/payouts/{batch_id}")
    if not response.ok:
        raise _error_from_response(response)
    return response.json()


def exchange_authorization_code(code: str, redirect_uri: str) -> dict:
    """Exchange OAuth 2.0 authorization code for user access token."""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise PayPalError("PayPal credentials are missing from .env", 500)

    try:
        response = requests.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=(CLIENT_ID, CLIENT_SECRET),
            headers={"Accept": "application/json"},
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            },
            timeout=TIMEOUT,
        )
    except requests.RequestException:
        raise PayPalError("Could not reach PayPal token service. Please try again.", 502)

    if not response.ok:
        raise _error_from_response(response)
    return response.json()


def get_user_info(user_access_token: str) -> dict:
    """Fetch authenticated user / merchant identity from OpenID Connect UserInfo endpoint."""
    try:
        response = requests.get(
            f"{PAYPAL_BASE_URL}/v1/identity/oauth2/userinfo",
            params={"schema": "openid"},
            headers={
                "Authorization": f"Bearer {user_access_token}",
                "Content-Type": "application/json",
            },
            timeout=TIMEOUT,
        )
    except requests.RequestException:
        raise PayPalError("Could not reach PayPal user info service. Please try again.", 502)

    if not response.ok:
        raise _error_from_response(response)
    return response.json()

