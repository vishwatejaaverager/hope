from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Donation

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
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_donation_history_pagination(client, db_session):
    for i in range(5):
        d = Donation(
            donor_name=f"Donor {i}",
            donor_email=f"donor{i}@example.com",
            amount=Decimal(f"{(i+1)*5}.00"),
            currency="USD",
            payment_provider="paypal",
            paypal_order_id=f"ORDER-{i}",
            paypal_capture_id=f"CAPTURE-{i}",
            payment_status="COMPLETED",
        )
        db_session.add(d)
    db_session.commit()

    res = client.get("/api/payments/history?limit=3&offset=0")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 5
    assert data["limit"] == 3
    assert data["offset"] == 0
    assert len(data["items"]) == 3

    res_page2 = client.get("/api/payments/history?limit=3&offset=3")
    assert res_page2.status_code == 200
    data_page2 = res_page2.json()
    assert len(data_page2["items"]) == 2
