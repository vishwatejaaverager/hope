import uuid
from unittest.mock import Mock
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Case, IncomingEmail, OutgoingEmail

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


def test_create_case_unauthorized(client):
    payload = {
        "patient_name": "John Doe",
        "patient_email": "john@example.com",
    }
    res = client.post("/api/v1/cases", json=payload)
    assert res.status_code == 401


def test_create_case_success_with_defaults(client, db_session):
    payload = {
        "patient_name": "Sarah Miller",
        "patient_email": "sarah.m@example.com",
        "medical_category": "upcoming_surgery",
        "treatment_description": "Cardiovascular surgery",
        "hospital_name": "City General Hospital",
        "estimated_cost": 25000.00,
        "requested_amount": 15000.00,
    }
    res = client.post(
        "/api/v1/cases",
        json=payload,
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res.status_code == 201
    data = res.json()

    assert data["patient_name"] == "Sarah Miller"
    assert data["medical_category"] == "upcoming_surgery"
    assert data["status"] == "new"
    assert data["urgency"] == "medium"
    assert data["currency"] == "USD"
    assert data["case_number"].startswith("CASE-")
    assert "id" in data

    case_uuid = uuid.UUID(data["id"])
    row = db_session.execute(select(Case).where(Case.id == case_uuid)).scalar_one_or_none()
    assert row is not None
    assert row.patient_name == "Sarah Miller"
    assert row.estimated_cost == Decimal("25000.00")


def test_list_and_filter_cases(client):
    # Create Case 1: critical surgery
    client.post(
        "/api/v1/cases",
        json={
            "case_number": "CASE-2026-AAA1",
            "patient_name": "Patient One",
            "patient_email": "p1@care.org",
            "medical_category": "upcoming_surgery",
            "status": "awaiting_documents",
            "urgency": "critical",
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    # Create Case 2: medication assistance
    client.post(
        "/api/v1/cases",
        json={
            "case_number": "CASE-2026-BBB2",
            "patient_name": "Patient Two",
            "patient_email": "p2@care.org",
            "medical_category": "medication_assistance",
            "status": "under_review",
            "urgency": "low",
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )

    # Filter by status
    res = client.get(
        "/api/v1/cases?status=awaiting_documents",
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["case_number"] == "CASE-2026-AAA1"

    # Filter by category
    res2 = client.get(
        "/api/v1/cases?medical_category=medication_assistance",
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res2.status_code == 200
    items2 = res2.json()
    assert len(items2) == 1
    assert items2[0]["case_number"] == "CASE-2026-BBB2"


def test_update_case_living_summary_and_status(client, db_session):
    res_create = client.post(
        "/api/v1/cases",
        json={"patient_name": "David Clark", "patient_email": "david@clark.org"},
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    case_id = res_create.json()["id"]

    res_patch = client.patch(
        f"/api/v1/cases/{case_id}",
        json={
            "status": "awaiting_documents",
            "overall_summary": "Patient requested $10,000 for emergency appendectomy. Identity received, awaiting hospital estimate.",
            "next_action": "Request hospital treatment estimate",
            "pending_items": ["hospital_treatment_estimate", "patient_authorization"],
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_patch.status_code == 200
    patched = res_patch.json()
    assert patched["status"] == "awaiting_documents"
    assert "emergency appendectomy" in patched["overall_summary"]
    assert patched["next_action"] == "Request hospital treatment estimate"
    assert "hospital_treatment_estimate" in patched["pending_items"]


def test_link_emails_and_chronological_timeline(client, db_session):
    # 1. Create a case
    res_case = client.post(
        "/api/v1/cases",
        json={"case_number": "CASE-TIMELINE-01", "patient_name": "Elena Rostova"},
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    case_id = res_case.json()["id"]
    case_uuid = uuid.UUID(case_id)

    # 2. Insert incoming email (t1 = 10:00)
    inc_email = IncomingEmail(
        message_id="<msg-inc-01@patient.org>",
        sender="elena@patient.org",
        recipient="applications@hope.org",
        subject="Assistance application",
        body_plain="Hello Hope, I need help with surgery bills.",
        received_at=datetime(2026, 11, 7, 10, 0, tzinfo=timezone.utc),
    )
    db_session.add(inc_email)

    # 3. Insert outgoing email (t2 = 11:30)
    out_email = OutgoingEmail(
        application_id="CASE-TIMELINE-01",
        recipient_email="elena@patient.org",
        subject="Re: Assistance application",
        body_plain="Dear Elena, please provide your hospital quote.",
        reply_to_message_id="<msg-inc-01@patient.org>",
        status="sent",
        created_at=datetime(2026, 11, 7, 11, 30, tzinfo=timezone.utc),
    )
    db_session.add(out_email)
    db_session.commit()
    db_session.refresh(inc_email)
    db_session.refresh(out_email)

    # 4. Link emails to case
    res_link = client.post(
        f"/api/v1/cases/{case_id}/link-email",
        json={
            "incoming_email_id": str(inc_email.id),
            "outgoing_email_id": str(out_email.id),
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_link.status_code == 200
    data = res_link.json()
    assert data["incoming_email_count"] == 1
    assert data["outgoing_email_count"] == 1
    assert len(data["timeline"]) == 2

    # Check chronological ordering: incoming first, outgoing second
    assert data["timeline"][0]["direction"] == "incoming"
    assert data["timeline"][0]["id"] == str(inc_email.id)
    assert data["timeline"][1]["direction"] == "outgoing"
    assert data["timeline"][1]["id"] == str(out_email.id)

    # 5. Query case detail by case_number
    res_by_num = client.get(
        "/api/v1/cases/CASE-TIMELINE-01",
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_by_num.status_code == 200
    assert len(res_by_num.json()["timeline"]) == 2


def test_auto_link_incoming_and_outgoing_emails_and_ai_summary(client, db_session):
    # 1. Create a case first
    res_case = client.post(
        "/api/v1/cases",
        json={
            "case_number": "CASE-2026-AUTO1",
            "patient_name": "Marcus Vance",
            "patient_email": "marcus@vance.org",
            "medical_category": "ongoing_hospitalization",
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_case.status_code == 201
    case_id = res_case.json()["id"]

    # 2. Receive incoming email referencing CASE-2026-AUTO1 in subject
    res_inc = client.post(
        "/api/v1/emails/incoming",
        json={
            "message_id": "<auto-inc-01@vance.org>",
            "sender": "marcus@vance.org",
            "recipient": "applications@hope.org",
            "subject": "Hospital documents for [CASE-2026-AUTO1]",
            "body_plain": "Attached is my interim hospital bill.",
            "received_at": "2026-11-07T08:00:00Z",
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_inc.status_code == 201
    inc_data = res_inc.json()
    assert inc_data["case_id"] == case_id
    assert inc_data["application_id"] == "CASE-2026-AUTO1"
    inc_email_id = inc_data["email_id"]

    # 3. Update attachment_metadata (documents list) on the incoming email
    res_patch_inc = client.patch(
        f"/api/v1/emails/incoming/{inc_email_id}",
        json={
            "attachment_metadata": [
                {"filename": "interim_hospital_bill.pdf", "url": "https://files.hope.org/interim_hospital_bill.pdf"}
            ]
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_patch_inc.status_code == 200
    assert res_patch_inc.json()["attachment_metadata"][0]["filename"] == "interim_hospital_bill.pdf"

    # 4. Send outbound email with application_id = CASE-2026-AUTO1
    res_out = client.post(
        "/api/v1/emails/send",
        json={
            "application_id": "CASE-2026-AUTO1",
            "recipient_email": "billing@generalhospital.org",
            "subject": "Verification Request - CASE-2026-AUTO1",
            "body": "Please confirm Marcus Vance hospitalization bill.",
            "reply_to_message_id": "<auto-inc-01@vance.org>",
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_out.status_code == 201
    assert res_out.json()["case_id"] == case_id

    # 5. Fetch case detail and verify incoming + auto-reply + explicit outbound emails + email_exchanges are in case
    res_detail = client.get(
        f"/api/v1/cases/{case_id}",
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["incoming_email_count"] == 1
    assert detail["outgoing_email_count"] == 2
    assert len(detail["timeline"]) == 3
    assert len(detail["email_exchanges"]) == 3
    assert detail["email_exchanges"][0]["id"] == inc_email_id
    assert detail["email_exchanges"][0]["direction"] == "incoming"


def test_incoming_email_auto_creates_case_and_ai_living_summary(client, db_session, monkeypatch):
    monkeypatch.setenv('DISABLE_OPENROUTER_IN_TESTS', '1')
    monkeypatch.setattr('app.api.routes.email.requests.post', Mock())
    monkeypatch.setattr('app.services.smtp_service.smtp_configured', lambda: False)
    monkeypatch.delenv("OPENROUTER_API", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    res_inc = client.post(
        "/api/v1/emails/incoming",
        json={
            "message_id": "<new-case-01@patient.org>",
            "sender": "Priya Nair <priya.nair@patient.org>",
            "recipient": "applications@hope.org",
            "subject": "Urgent surgery assistance needed",
            "body_plain": "Hello Hope team, I have an upcoming surgery at Apollo Hospital costing $12,500 and need urgent financial assistance.",
            "attachments": [
                {
                    "filename": "apollo_estimate.pdf",
                    "url": "https://files.hope.org/apollo_estimate.pdf",
                    "content_type": "application/pdf",
                    "size": 40960,
                }
            ],
            "received_at": "2026-11-07T09:00:00Z",
        },
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_inc.status_code == 201
    inc_data = res_inc.json()
    assert inc_data["case_id"] is not None
    assert inc_data["application_id"].startswith("CASE-")

    # Verify the auto-created case has AI living summary, email_exchanges & auto-reply queued
    res_case = client.get(
        f"/api/v1/cases/{inc_data['case_id']}",
        headers={"X-Webhook-Secret": TEST_SECRET},
    )
    assert res_case.status_code == 200
    case_data = res_case.json()
    assert case_data["patient_name"] == "Priya Nair"
    assert case_data["patient_email"] == "priya.nair@patient.org"
    assert case_data["medical_category"] == "upcoming_surgery"
    assert case_data["urgency"] in ("high", "critical")
    assert float(case_data["estimated_cost"]) == 12500.0
    assert case_data["overall_summary"] is not None
    assert case_data["next_action"] is not None
    assert case_data["incoming_email_count"] == 1
    assert case_data["outgoing_email_count"] == 1  # Auto-reply email queued automatically!
    assert len(case_data["timeline"]) == 2
    assert len(case_data["email_exchanges"]) == 2
    assert case_data["email_exchanges"][0]["id"] == inc_data["email_id"]
    assert case_data["email_exchanges"][0]["direction"] == "incoming"
    assert case_data["email_exchanges"][1]["direction"] == "outgoing"
    assert case_data["timeline"][0]["attachments"][0]["filename"] == "apollo_estimate.pdf"
    assert case_data["timeline"][0]["attachments"][0]["url"] == "https://files.hope.org/apollo_estimate.pdf"
    assert case_data["timeline"][1]["direction"] == "outgoing"
    assert case_data["timeline"][1]["recipient"] == "priya.nair@patient.org"


