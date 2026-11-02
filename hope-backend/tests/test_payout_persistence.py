import uuid
from decimal import Decimal
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.routes.auth import require_admin_session
from app.db import Base, get_db
from app.main import app
from app.models import Payout

# Use an in-memory SQLite database for test isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
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
    app.dependency_overrides[require_admin_session] = lambda: {"sub": "TEST_MERCHANT"}
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_payout_persists_initial_status(client, db_session):
    batch_id = "BATCH-TEST-001"
    item_id = "ITEM-TEST-001"

    paypal_created_response = {
        "batch_header": {
            "payout_batch_id": batch_id,
            "batch_status": "PENDING",
        }
    }
    paypal_get_response = {
        "batch_header": {
            "payout_batch_id": batch_id,
            "batch_status": "PENDING",
        },
        "items": [
            {
                "payout_item_id": item_id,
                "transaction_status": "PENDING",
                "payout_item": {
                    "amount": {"value": "5.00", "currency": "USD"},
                    "receiver": "beneficiary@example.com",
                },
            }
        ],
    }

    with patch("app.services.paypal_service.create_payout", return_value=paypal_created_response):
        with patch("app.services.paypal_service.get_payout", return_value=paypal_get_response):
            response = client.post(
                "/api/payouts/create",
                json={
                    "beneficiary_name": "John Doe",
                    "email": "beneficiary@example.com",
                    "amount": "5.00",
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert data["batch_id"] == batch_id
    assert data["batch_status"] == "PENDING"
    assert data["item_status"] == "PENDING"
    assert data["paid"] is False
    assert data["final"] is False

    # Check persistence in database
    row = db_session.execute(
        select(Payout).where(Payout.paypal_batch_id == batch_id)
    ).scalar_one_or_none()
    assert row is not None
    assert row.beneficiary_name == "John Doe"
    assert row.recipient_email == "beneficiary@example.com"
    assert row.amount == Decimal("5.00")
    assert row.currency == "USD"
    assert row.payment_provider == "paypal"
    assert row.paypal_batch_id == batch_id
    assert row.paypal_item_id == item_id
    assert row.batch_status == "PENDING"
    assert row.item_status == "PENDING"
    assert row.raw_response == paypal_get_response


def test_batch_success_does_not_mark_paid_if_item_not_success(client, db_session):
    """Batch header might say SUCCESS while item is UNCLAIMED or PENDING."""
    batch_id = "BATCH-TEST-002"
    item_id = "ITEM-TEST-002"

    paypal_created_response = {
        "batch_header": {"payout_batch_id": batch_id, "batch_status": "PENDING"}
    }
    paypal_get_response = {
        "batch_header": {"payout_batch_id": batch_id, "batch_status": "SUCCESS"},
        "items": [
            {
                "payout_item_id": item_id,
                "transaction_status": "UNCLAIMED",
                "payout_item": {
                    "amount": {"value": "2.00", "currency": "USD"},
                    "receiver": "newuser@example.com",
                },
            }
        ],
    }

    with patch("app.services.paypal_service.create_payout", return_value=paypal_created_response):
        with patch("app.services.paypal_service.get_payout", return_value=paypal_get_response):
            response = client.post(
                "/api/payouts/create",
                json={
                    "beneficiary_name": "Jane Doe",
                    "email": "newuser@example.com",
                    "amount": "2.00",
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert data["batch_status"] == "SUCCESS"
    assert data["item_status"] == "UNCLAIMED"
    assert data["paid"] is False  # Must not be marked paid!
    assert data["final"] is True

    row = db_session.execute(
        select(Payout).where(Payout.paypal_batch_id == batch_id)
    ).scalar_one_or_none()
    assert row.item_status == "UNCLAIMED"


def test_payout_lookup_by_batch_id_syncs_status_and_marks_success(client, db_session):
    batch_id = "BATCH-TEST-003"
    item_id = "ITEM-TEST-003"

    initial_payout = Payout(
        beneficiary_name="Alice Smith",
        recipient_email="alice@example.com",
        amount=Decimal("1.00"),
        currency="USD",
        payment_provider="paypal",
        paypal_batch_id=batch_id,
        paypal_item_id=item_id,
        batch_status="PENDING",
        item_status="PENDING",
    )
    db_session.add(initial_payout)
    db_session.commit()

    updated_paypal_response = {
        "batch_header": {"payout_batch_id": batch_id, "batch_status": "SUCCESS"},
        "items": [
            {
                "payout_item_id": item_id,
                "transaction_id": "TX-PAYPAL-123",
                "transaction_status": "SUCCESS",
                "payout_item": {
                    "amount": {"value": "1.00", "currency": "USD"},
                    "receiver": "alice@example.com",
                },
            }
        ],
    }

    with patch("app.services.paypal_service.get_payout", return_value=updated_paypal_response):
        response = client.get(f"/api/payouts/{batch_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["batch_status"] == "SUCCESS"
    assert data["item_status"] == "SUCCESS"
    assert data["paid"] is True
    assert data["final"] is True

    # Check that database record was updated in place, no duplicate row
    rows = db_session.execute(
        select(Payout).where(Payout.paypal_batch_id == batch_id)
    ).scalars().all()
    assert len(rows) == 1
    assert rows[0].batch_status == "SUCCESS"
    assert rows[0].item_status == "SUCCESS"
    assert rows[0].paypal_transaction_id == "TX-PAYPAL-123"


def test_payout_lookup_by_db_uuid(client, db_session):
    payout_id = uuid.uuid4()
    payout = Payout(
        id=payout_id,
        beneficiary_name="Bob Jones",
        recipient_email="bob@example.com",
        amount=Decimal("10.00"),
        currency="USD",
        payment_provider="paypal",
        paypal_batch_id="BATCH-TEST-UUID",
        paypal_item_id="ITEM-TEST-UUID",
        batch_status="SUCCESS",
        item_status="SUCCESS",
    )
    db_session.add(payout)
    db_session.commit()

    response = client.get(f"/api/payouts/{payout_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(payout_id)
    assert data["beneficiary_name"] == "Bob Jones"
    assert data["recipient_email"] == "bob@example.com"
    assert data["amount"] == "10.00"
    assert data["paypal_batch_id"] == "BATCH-TEST-UUID"

    # Non-existent UUID
    missing_id = uuid.uuid4()
    resp_missing = client.get(f"/api/payouts/{missing_id}")
    assert resp_missing.status_code == 404
    assert resp_missing.json()["detail"] == "Payout record not found"


def test_payout_history(client, db_session):
    for i in range(5):
        p = Payout(
            beneficiary_name=f"Beneficiary {i}",
            recipient_email=f"user{i}@example.com",
            amount=Decimal(f"{(i+1)*2}.00"),
            currency="USD",
            payment_provider="paypal",
            paypal_batch_id=f"BATCH-HIST-{i}",
            paypal_item_id=f"ITEM-HIST-{i}",
            batch_status="SUCCESS",
            item_status="SUCCESS",
        )
        db_session.add(p)
    db_session.commit()

    response = client.get("/api/payouts/history?limit=3&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 5
    assert data["limit"] == 3
    assert data["offset"] == 0
    assert len(data["items"]) == 3

    # Check offset
    resp_page2 = client.get("/api/payouts/history?limit=3&offset=3")
    assert resp_page2.status_code == 200
    data_page2 = resp_page2.json()
    assert len(data_page2["items"]) == 2


def test_create_payout_validation_errors(client):
    # Empty beneficiary name
    resp1 = client.post(
        "/api/payouts/create",
        json={"beneficiary_name": "", "email": "valid@example.com", "amount": "1.00"},
    )
    assert resp1.status_code == 422

    # Invalid email
    resp2 = client.post(
        "/api/payouts/create",
        json={"beneficiary_name": "Valid Name", "email": "invalid-email", "amount": "1.00"},
    )
    assert resp2.status_code == 422

    # Amount <= 0
    resp3 = client.post(
        "/api/payouts/create",
        json={"beneficiary_name": "Valid Name", "email": "valid@example.com", "amount": "0.00"},
    )
    assert resp3.status_code == 422

    # Amount > 100
    resp4 = client.post(
        "/api/payouts/create",
        json={"beneficiary_name": "Valid Name", "email": "valid@example.com", "amount": "150.00"},
    )
    assert resp4.status_code == 422
