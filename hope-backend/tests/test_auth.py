from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

from app.core.security import (
    SESSION_COOKIE_NAME,
    STATE_COOKIE_NAME,
    create_session_token,
    generate_csrf_state,
)
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_auth_login_redirects_to_paypal(client):
    res = client.get("/api/auth/login", follow_redirects=False)
    assert res.status_code == 302
    location = res.headers.get("location", "")
    assert "paypal.com/signin/authorize" in location
    assert "response_type=code" in location
    assert "scope=" in location
    assert STATE_COOKIE_NAME in res.cookies


def test_auth_callback_fails_with_csrf_mismatch(client):
    state = generate_csrf_state()
    # Sending query state that doesn't match cookie
    res = client.get(
        f"/api/auth/callback?code=mock_code&state={state}",
        cookies={STATE_COOKIE_NAME: "different_state"},
        follow_redirects=False,
    )
    assert res.status_code == 302
    assert "error=csrf_validation_failed" in res.headers.get("location", "")


def test_auth_callback_success(client):
    state = generate_csrf_state()

    mock_token = {"access_token": "mock_user_access_token"}
    mock_userinfo = {
        "payer_id": "MERCHANT_123",
        "email": "merchant@hope.org",
        "name": "Hope Administrator",
    }

    with patch("app.services.paypal_service.exchange_authorization_code", return_value=mock_token):
        with patch("app.services.paypal_service.get_user_info", return_value=mock_userinfo):
            res = client.get(
                f"/api/auth/callback?code=valid_code&state={state}",
                cookies={STATE_COOKIE_NAME: state},
                follow_redirects=False,
            )
            assert res.status_code == 302
            assert "/dashboard" in res.headers.get("location", "")
            assert SESSION_COOKIE_NAME in res.cookies


def test_auth_callback_rejects_unauthorized_merchant(client, monkeypatch):
    monkeypatch.setenv("AUTHORIZED_PAYPAL_MERCHANT_ID", "ALLOWED_MERCHANT_456")
    from app.api.routes import auth
    monkeypatch.setattr(auth, "AUTHORIZED_PAYPAL_MERCHANT_ID", "ALLOWED_MERCHANT_456")

    state = generate_csrf_state()
    mock_token = {"access_token": "mock_user_access_token"}
    mock_userinfo = {
        "payer_id": "DIFFERENT_MERCHANT_999",
        "email": "intruder@example.com",
        "name": "Intruder",
    }

    with patch("app.services.paypal_service.exchange_authorization_code", return_value=mock_token):
        with patch("app.services.paypal_service.get_user_info", return_value=mock_userinfo):
            res = client.get(
                f"/api/auth/callback?code=valid_code&state={state}",
                cookies={STATE_COOKIE_NAME: state},
                follow_redirects=False,
            )
            assert res.status_code == 302
            assert "error=unauthorized_merchant" in res.headers.get("location", "")
            assert SESSION_COOKIE_NAME not in res.cookies


def test_auth_me_authenticated_and_logout(client):
    # Unauthenticated
    unauth = client.get("/api/auth/me")
    assert unauth.status_code == 401

    # Authenticated with session cookie
    token = create_session_token(merchant_id="MERCHANT_123", email="merchant@hope.org", name="Admin")
    auth_res = client.get("/api/auth/me", cookies={SESSION_COOKIE_NAME: token})
    assert auth_res.status_code == 200
    data = auth_res.json()
    assert data["authenticated"] is True
    assert data["merchant_id"] == "MERCHANT_123"
    assert data["email"] == "merchant@hope.org"

    # Logout
    logout_res = client.post("/api/auth/logout")
    assert logout_res.status_code == 200


def test_login_credentials_success(client):
    res = client.post(
        "/api/auth/login-credentials",
        json={"email": "admin@hope.org", "password": "admin123"},
    )
    assert res.status_code == 200
    assert SESSION_COOKIE_NAME in res.cookies


def test_login_credentials_invalid(client):
    res = client.post(
        "/api/auth/login-credentials",
        json={"email": "wrong@hope.org", "password": "badpassword"},
    )
    assert res.status_code == 401
    assert SESSION_COOKIE_NAME not in res.cookies

