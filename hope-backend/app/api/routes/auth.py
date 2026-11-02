import logging
import os
import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse

from app.core.security import (
    SESSION_COOKIE_NAME,
    SESSION_DURATION_SECONDS,
    STATE_COOKIE_NAME,
    STATE_DURATION_SECONDS,
    create_session_token,
    generate_csrf_state,
    verify_csrf_state,
    verify_session_token,
)
from app.services import paypal_service
from app.services.paypal_service import PayPalError

from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])

PAYPAL_AUTHORIZATION_URL = os.getenv(
    "PAYPAL_AUTHORIZATION_URL", "https://www.sandbox.paypal.com/signin/authorize"
).rstrip("/")
PAYPAL_REDIRECT_URI = os.getenv(
    "PAYPAL_REDIRECT_URI", "http://localhost:8000/api/auth/callback"
)
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "http://localhost:3000").rstrip("/")
AUTHORIZED_PAYPAL_MERCHANT_ID = os.getenv("AUTHORIZED_PAYPAL_MERCHANT_ID", "").strip()


class LoginCredentialsRequest(BaseModel):
    email: str
    password: str


def require_admin_session(request: Request) -> dict:
    """FastAPI dependency to protect admin endpoints."""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        # Also check Authorization header for API clients: Bearer <token>
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please sign in.",
        )

    payload = verify_session_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Session expired or invalid. Please sign in again.",
        )

    # Validate against authorized merchant ID if configured (skip for master admin)
    merchant_id = payload.get("sub")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@hope.org").strip().lower()
    is_master_admin = merchant_id == "ADMIN_PRIMARY" or (
        payload.get("email") and payload.get("email").lower() == admin_email
    )

    if not is_master_admin and AUTHORIZED_PAYPAL_MERCHANT_ID and merchant_id != AUTHORIZED_PAYPAL_MERCHANT_ID:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Authenticated PayPal account is not authorized.",
        )

    return payload


@router.post("/login-credentials")
def login_credentials(body: LoginCredentialsRequest, request: Request, response: Response):
    """Direct email + password authentication for Hope Admin."""
    admin_email = os.getenv("ADMIN_EMAIL", "admin@hope.org").strip().lower()
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123").strip()

    if body.email.strip().lower() != admin_email or body.password != admin_password:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    session_token = create_session_token(
        merchant_id="ADMIN_PRIMARY",
        email=admin_email,
        name="Hope Administrator",
    )
    is_secure = request.url.scheme == "https"
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_token,
        httponly=True,
        samesite="lax",
        secure=is_secure,
        max_age=SESSION_DURATION_SECONDS,
        path="/",
    )
    return {"success": True, "message": "Authenticated successfully"}


@router.get("/login")
def login(request: Request):
    """Initiates PayPal OAuth 2.0 Authorization Code flow."""
    try:
        client_id = paypal_service.get_client_id()
    except PayPalError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    state = generate_csrf_state()
    params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": PAYPAL_REDIRECT_URI,
        "state": state,
    }
    auth_url = f"{PAYPAL_AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"

    is_secure = request.url.scheme == "https"
    response = RedirectResponse(auth_url, status_code=302)
    response.set_cookie(
        key=STATE_COOKIE_NAME,
        value=state,
        httponly=True,
        samesite="lax",
        secure=is_secure,
        max_age=STATE_DURATION_SECONDS,
        path="/",
    )
    return response


@router.get("/callback")
def oauth_callback(
    request: Request,
    code: str = None,
    state: str = None,
    error: str = None,
    error_description: str = None,
):
    """Handles OAuth 2.0 redirect from PayPal."""
    is_secure = request.url.scheme == "https"

    if error:
        logger.warning("PayPal OAuth returned error: %s (%s)", error, error_description)
        err_msg = urllib.parse.quote(error_description or error)
        return RedirectResponse(f"{DASHBOARD_URL}/login?error={err_msg}", status_code=302)

    if not code or not state:
        return RedirectResponse(f"{DASHBOARD_URL}/login?error=missing_code_or_state", status_code=302)

    # CSRF State verification
    cookie_state = request.cookies.get(STATE_COOKIE_NAME)
    if not cookie_state or state != cookie_state or not verify_csrf_state(state):
        logger.warning("OAuth CSRF state validation failed.")
        return RedirectResponse(f"{DASHBOARD_URL}/login?error=csrf_validation_failed", status_code=302)

    # Exchange code for user access token
    try:
        token_data = paypal_service.exchange_authorization_code(code, PAYPAL_REDIRECT_URI)
        user_access_token = token_data.get("access_token")
        if not user_access_token:
            logger.error("No access token in PayPal token exchange response.")
            return RedirectResponse(f"{DASHBOARD_URL}/login?error=token_exchange_failed", status_code=302)
    except PayPalError as exc:
        logger.error("Failed to exchange PayPal authorization code: %s", exc.message)
        return RedirectResponse(f"{DASHBOARD_URL}/login?error={urllib.parse.quote(exc.message)}", status_code=302)

    # Retrieve user info from PayPal Identity service
    try:
        user_info = paypal_service.get_user_info(user_access_token)
    except PayPalError as exc:
        logger.error("Failed to fetch PayPal userinfo: %s", exc.message)
        return RedirectResponse(f"{DASHBOARD_URL}/login?error={urllib.parse.quote(exc.message)}", status_code=302)

    # Extract merchant account / payer ID
    raw_user_id = user_info.get("payer_id") or user_info.get("user_id") or ""
    payer_id = raw_user_id.rstrip("/").split("/")[-1] if "/" in raw_user_id else raw_user_id
    email = user_info.get("email")
    name = user_info.get("name")

    logger.info("PayPal authenticated merchant: payer_id=%s, email=%s, name=%s", payer_id, email, name)

    # Compare against AUTHORIZED_PAYPAL_MERCHANT_ID
    if AUTHORIZED_PAYPAL_MERCHANT_ID:
        if payer_id != AUTHORIZED_PAYPAL_MERCHANT_ID and raw_user_id != AUTHORIZED_PAYPAL_MERCHANT_ID:
            logger.warning(
                "Unauthorized merchant attempted access: got %s, expected %s",
                payer_id,
                AUTHORIZED_PAYPAL_MERCHANT_ID,
            )
            redirect = RedirectResponse(
                f"{DASHBOARD_URL}/login?error=unauthorized_merchant&merchant_id={urllib.parse.quote(payer_id)}",
                status_code=302,
            )
            redirect.delete_cookie(key=STATE_COOKIE_NAME, path="/")
            return redirect

    # Create signed session
    session_token = create_session_token(merchant_id=payer_id, email=email, name=name)

    redirect = RedirectResponse(f"{DASHBOARD_URL}/dashboard", status_code=302)
    redirect.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_token,
        httponly=True,
        samesite="lax",
        secure=is_secure,
        max_age=SESSION_DURATION_SECONDS,
        path="/",
    )
    redirect.delete_cookie(key=STATE_COOKIE_NAME, path="/")
    return redirect


@router.get("/me")
def me(session: dict = Depends(require_admin_session)):
    """Returns the authenticated merchant's profile."""
    return {
        "authenticated": True,
        "merchant_id": session.get("sub"),
        "email": session.get("email"),
        "name": session.get("name"),
    }


@router.post("/logout")
def logout(response: Response):
    """Clears the admin session cookie."""
    response = JSONResponse({"success": True, "message": "Successfully logged out."})
    response.delete_cookie(key=SESSION_COOKIE_NAME, path="/")
    return response
