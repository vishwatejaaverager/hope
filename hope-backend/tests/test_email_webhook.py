import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import IncomingEmail

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

TEST_SECRET = "test-webhook-secret-12345"


@pytest.fixture(scope="function", autouse=True)
def setup_database(monkeypatch):
    monkeypatch.setenv("EMAIL_WEBHOOK_SECRET", TEST_SECRET)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_incoming_email_unauthorized_without_secret(client):
    payload = {
        "message_id": "<msg-001@mail.example.com>",
        "sender": "applicant@example.com",
        "recipient": "support@hope.org",
        "subject": "Medical bill submission",
        "body_plain": "Please find attached document.",
    }
    res = client.post("/api/v1/emails/incoming", json=payload)
    assert res.status_code == 401
    assert "Invalid or missing webhook secret" in res.json()["detail"]


def test_incoming_email_unauthorized_with_wrong_secret(client):
    payload = {
        "message_id": "<msg-002@mail.example.com>",
        "sender": "applicant@example.com",
        "recipient": "support@hope.org",
    }
    res = client.post(
        "/api/v1/emails/incoming",
        json=payload,
        headers={"X-Webhook-Secret": "wrong-secret"},
    )
    assert res.status_code == 401


def test_incoming_email_success_with_header_secret(client, db_session):
    payload = {
        "message_id": "<msg-003@mail.example.com>",
        "sender": "patient@hospital.org",
        "recipient": "applications@hope.org",
        "subject": "Treatment application [APP-9921]",
        "body_plain": "Attached is the estimate for surgery.",
        "body_html": "<p>Attached is the estimate for surgery.</p>",
        "received_at": "2026-11-03T10:00:00Z",
        "attachments": [
            {
                "filename": "surgery_quote.pdf",
                "content_type": "application/pdf",
                "size": 102400,
                "url": "https://cdn.example.com/files/surgery_quote.pdf",
            }
        ],
    }

    res = client.post(
        "/api/v1/emails/incoming",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )

    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "received"
    assert data["duplicate"] is False
    assert data["message_id"] == "<msg-003@mail.example.com>"
    assert data["application_id"] == "APP-9921"
    assert data["email_id"] is not None

    # Verify database persistence
    saved = db_session.query(IncomingEmail).filter_by(message_id="<msg-003@mail.example.com>").one()
    assert saved.sender == "patient@hospital.org"
    assert saved.recipient == "applications@hope.org"
    assert saved.subject == "Treatment application [APP-9921]"
    assert saved.body_plain == "Attached is the estimate for surgery."
    assert saved.body_html == "<p>Attached is the estimate for surgery.</p>"
    assert saved.attachment_count == 1
    assert saved.attachment_metadata[0]["filename"] == "surgery_quote.pdf"
    assert saved.application_id == "APP-9921"


def test_incoming_email_secret_in_query_param(client):
    payload = {
        "message_id": "<msg-004@mail.example.com>",
        "sender": "patient2@hospital.org",
        "recipient": "applications@hope.org",
        "subject": "Case details",
        "body_plain": "Hello, here is my case.",
    }

    res = client.post(f"/api/v1/emails/incoming?secret={TEST_SECRET}", json=payload)
    assert res.status_code == 201
    assert res.json()["status"] == "received"


def test_incoming_email_secret_in_payload_body(client):
    payload = {
        "webhook_secret": TEST_SECRET,
        "message_id": "<msg-005@mail.example.com>",
        "sender": "patient3@hospital.org",
        "recipient": "applications@hope.org",
        "subject": "Case details",
        "body_plain": "Hello, here is my case.",
    }

    res = client.post("/api/v1/emails/incoming", json=payload)
    assert res.status_code == 201
    assert res.json()["status"] == "received"


def test_incoming_email_deduplication(client, db_session):
    payload = {
        "message_id": "<unique-dedup-msg-123@mail.example.com>",
        "sender": "patient@hospital.org",
        "recipient": "applications@hope.org",
        "subject": "First submission",
        "body_plain": "Initial submission text.",
        "application_id": "APP-5555",
    }

    # First delivery
    res1 = client.post(
        "/api/v1/emails/incoming",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res1.status_code == 201
    data1 = res1.json()
    assert data1["duplicate"] is False
    email_id = data1["email_id"]

    # Duplicate delivery with identical message_id
    res2 = client.post(
        "/api/v1/emails/incoming",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    # Should return 200 OK without creating another DB entry
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["duplicate"] is True
    assert data2["status"] == "already_processed"
    assert data2["email_id"] == email_id

    # Verify only 1 row exists in DB
    rows = db_session.query(IncomingEmail).filter_by(message_id="<unique-dedup-msg-123@mail.example.com>").all()
    assert len(rows) == 1


def test_incoming_email_zapier_field_normalization(client):
    # Zapier often sends from, to, text, messageId instead of snake_case
    zapier_payload = {
        "messageId": "<zapier-msg-999@mail.example.com>",
        "from": "applicant_zapier@example.com",
        "to": "help@hope.org",
        "Subject": "Re: Medical Grant [BEN-7788]",
        "text": "Sent from Zapier parser.",
        "attachments": [
            {"filename": "bill1.jpg", "size": 50000},
            {"filename": "bill2.jpg", "size": 65000},
        ],
    }

    res = client.post(
        "/api/v1/emails/incoming",
        json=zapier_payload,
        headers={"X-Zapier-Secret": TEST_SECRET},
    )

    assert res.status_code == 201
    data = res.json()
    assert data["message_id"] == "<zapier-msg-999@mail.example.com>"
    assert data["application_id"] == "BEN-7788"


def test_incoming_email_extracts_application_id_from_body(client, db_session):
    payload = {
        "message_id": "<body-extract-msg@mail.example.com>",
        "sender": "applicant@example.com",
        "recipient": "help@hope.org",
        "subject": "Invoice for review",
        "body_plain": "Hello, my application number: APP-43210. Please process.",
    }

    res = client.post(
        "/api/v1/emails/incoming",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )

    assert res.status_code == 201
    data = res.json()
    assert data["application_id"] == "APP-43210"

    saved = db_session.query(IncomingEmail).filter_by(message_id="<body-extract-msg@mail.example.com>").one()
    assert saved.application_id == "APP-43210"


def test_incoming_email_rfc2822_date_format(client, db_session):
    """Verify that email RFC 2822 format (e.g. 'Tue, 03 Nov 2026 09:30:15 +0000') parses cleanly."""
    payload = {
        "message_id": "<rfc2822-test-msg@mail.example.com>",
        "sender": "applicant@example.com",
        "recipient": "help@hope.org",
        "subject": "Email with RFC date",
        "body_plain": "Test body",
        "Date": "Tue, 03 Nov 2026 09:30:15 +0000",
    }

    res = client.post(
        "/api/v1/emails/incoming",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )

    assert res.status_code == 201
    saved = db_session.query(IncomingEmail).filter_by(message_id="<rfc2822-test-msg@mail.example.com>").one()
    assert saved.received_at.year == 2026
    assert saved.received_at.month == 11
    assert saved.received_at.day == 3


def test_incoming_email_human_or_unparseable_date_fallback(client, db_session):
    """Verify that human or unexpected date strings fall back gracefully without 422 error."""
    payload = {
        "message_id": "<human-date-test-msg@mail.example.com>",
        "sender": "applicant@example.com",
        "recipient": "help@hope.org",
        "subject": "Email with human date",
        "date": "November 3rd 2026, 9:30:00 am",
    }

    res = client.post(
        "/api/v1/emails/incoming",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )

    assert res.status_code == 201
    saved = db_session.query(IncomingEmail).filter_by(message_id="<human-date-test-msg@mail.example.com>").one()
    assert saved.received_at is not None
