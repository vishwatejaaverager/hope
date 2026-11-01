import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import JSON, DateTime, Numeric, String, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Donation(Base):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(primary_key=True)
    donor_name: Mapped[Optional[str]] = mapped_column(String(255))
    donor_email: Mapped[Optional[str]] = mapped_column(String(255))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3))
    payment_provider: Mapped[str] = mapped_column(String(32), default="paypal")
    paypal_order_id: Mapped[str] = mapped_column(String(64), unique=True)
    paypal_capture_id: Mapped[Optional[str]] = mapped_column(String(64), unique=True)
    payment_status: Mapped[str] = mapped_column(String(32), default="CREATED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Payout(Base):
    __tablename__ = "payouts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    beneficiary_name: Mapped[Optional[str]] = mapped_column(String(255))
    recipient_email: Mapped[str] = mapped_column(String(255))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3))
    payment_provider: Mapped[str] = mapped_column(String(32), default="paypal")
    paypal_batch_id: Mapped[str] = mapped_column(String(64), unique=True)
    paypal_item_id: Mapped[Optional[str]] = mapped_column(String(64), unique=True)
    paypal_transaction_id: Mapped[Optional[str]] = mapped_column(String(64))
    batch_status: Mapped[str] = mapped_column(String(32))
    item_status: Mapped[Optional[str]] = mapped_column(String(32))
    raw_response: Mapped[Optional[Any]] = mapped_column(JSON().with_variant(JSONB, "postgresql"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
