import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import IncomingEmail, OutgoingEmail

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


def test_send_outbound_email_unauthorized_missing_secret(client):
    payload = {
        "application_id": "APP-2026-001",
        "recipient_email": "billing@cityhospital.org",
        "subject": "Verification for Treatment - APP-2026-001",
        "body": "Please confirm the patient treatment estimate.",
    }
    res = client.post("/api/v1/emails/send", json=payload)
    assert res.status_code == 401
    assert "Invalid or missing webhook secret" in res.json()["detail"]


def test_send_outbound_email_unauthorized_wrong_secret(client):
    payload = {
        "application_id": "APP-2026-001",
        "recipient_email": "billing@cityhospital.org",
        "subject": "Verification for Treatment - APP-2026-001",
        "body": "Please confirm the patient treatment estimate.",
    }
    res = client.post(
        "/api/v1/emails/send",
        json=payload,
        headers={"X-Webhook-Secret": "invalid-secret"},
    )
    assert res.status_code == 401


def test_send_outbound_email_success(client, db_session):
    payload = {
        "application_id": "APP-2026-789",
        "recipient_email": "accounts@hospital.org",
        "subject": "Urgent verification request for Patient Sarah",
        "body": "Dear Hospital Administrator, please verify the surgical estimate.",
        "body_html": "<p>Dear Hospital Administrator, please verify the surgical estimate.</p>",
        "reply_to_message_id": "<inquiry-123@hospital.org>",
        "correlation_id": "CORR-9999",
    }
    res = client.post(
        "/api/v1/emails/send",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res.status_code == 201
    data = res.json()

    assert data["status"] == "pending"
    assert data["application_id"] == "APP-2026-789"
    assert data["recipient_email"] == "accounts@hospital.org"
    assert data["subject"] == "Urgent verification request for Patient Sarah"
    assert data["reply_to_message_id"] == "<inquiry-123@hospital.org>"
    assert data["correlation_id"] == "CORR-9999"
    assert "email_id" in data

    email_uuid = uuid.UUID(data["email_id"])
    record = db_session.execute(
        select(OutgoingEmail).where(OutgoingEmail.id == email_uuid)
    ).scalar_one_or_none()

    assert record is not None
    assert record.application_id == "APP-2026-789"
    assert record.recipient_email == "accounts@hospital.org"
    assert record.status == "pending"
    assert record.body_plain == "Dear Hospital Administrator, please verify the surgical estimate."
    assert record.body_html == "<p>Dear Hospital Administrator, please verify the surgical estimate.</p>"
    assert record.reply_to_message_id == "<inquiry-123@hospital.org>"
    assert record.correlation_id == "CORR-9999"
    assert record.sent_at is None


def test_send_outbound_email_field_normalization(client, db_session):
    payload = {
        "app_id": "APP-4040",
        "to": "doctor@clinic.org",
        "subject": "Verification Case APP-4040",
        "text": "Doctor, please confirm beneficiary diagnosis.",
        "in_reply_to": "<msg-0040@mail.clinic.org>",
        "tracking_id": "TRACK-555",
        "secret": TEST_SECRET,
    }
    res = client.post("/api/v1/emails/send", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["application_id"] == "APP-4040"
    assert data["recipient_email"] == "doctor@clinic.org"
    assert data["reply_to_message_id"] == "<msg-0040@mail.clinic.org>"
    assert data["correlation_id"] == "TRACK-555"


def test_send_outbound_email_invalid_recipient_format(client):
    payload = {
        "application_id": "APP-1111",
        "recipient_email": "invalid-email-address",
        "subject": "Verification",
        "body": "Test message.",
    }
    res = client.post(
        "/api/v1/emails/send",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res.status_code == 422


def test_list_and_update_pending_emails(client):
    # Queue two emails
    client.post(
        "/api/v1/emails/send",
        json={
            "application_id": "APP-101",
            "recipient_email": "hospital1@care.org",
            "subject": "Verification 1",
            "body": "Body 1",
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    res2 = client.post(
        "/api/v1/emails/send",
        json={
            "application_id": "APP-102",
            "recipient_email": "hospital2@care.org",
            "subject": "Verification 2",
            "body": "Body 2",
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    email_id2 = res2.json()["email_id"]

    # Poll pending list
    res_list = client.get(
        "/api/v1/emails/pending",
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_list.status_code == 200
    items = res_list.json()
    assert len(items) == 2
    assert all(item["status"] == "pending" for item in items)

    # Update status of email 2 to sent
    res_patch = client.patch(
        f"/api/v1/emails/{email_id2}/status",
        json={
            "status": "sent",
            "sent_message_id": "<hostinger-dispatch-102@mail.hope.org>",
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_patch.status_code == 200
    patched_data = res_patch.json()
    assert patched_data["status"] == "sent"
    assert patched_data["correlation_id"] == "<hostinger-dispatch-102@mail.hope.org>"

    # Check pending list again: should only have 1 pending
    res_list_after = client.get(
        "/api/v1/emails/pending",
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    items_after = res_list_after.json()
    assert len(items_after) == 1
    assert items_after[0]["application_id"] == "APP-101"


def test_existing_incoming_email_endpoint_unaffected(client):
    payload = {
        "message_id": "<incoming-check-999@mail.example.com>",
        "sender": "applicant@test.com",
        "recipient": "support@hope.org",
        "subject": "Support inquiry [APP-7070]",
        "body_plain": "Please check status of application.",
    }
    res = client.post(
        "/api/v1/emails/incoming",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res.status_code == 201
    assert res.json()["status"] == "received"
    assert res.json()["application_id"] == "APP-7070"
