import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, Numeric, String, Text, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    case_number: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    patient_user_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    patient_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    patient_email: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    medical_category: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)
    treatment_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hospital_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    estimated_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    requested_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    urgency: Mapped[str] = mapped_column(String(32), default="medium", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="new", index=True, nullable=False)
    overall_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    next_action: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    pending_items: Mapped[Optional[Any]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    email_exchanges: Mapped[Optional[Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=list, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    incoming_emails: Mapped[list["IncomingEmail"]] = relationship(
        "IncomingEmail", back_populates="case", order_by="IncomingEmail.received_at"
    )
    outgoing_emails: Mapped[list["OutgoingEmail"]] = relationship(
        "OutgoingEmail", back_populates="case", order_by="OutgoingEmail.created_at"
    )


class IncomingEmail(Base):
    __tablename__ = "incoming_emails"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid, ForeignKey("cases.id", ondelete="SET NULL"), nullable=True, index=True
    )
    message_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    sender: Mapped[str] = mapped_column(String(255), nullable=False)
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    body_plain: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    body_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attachment_metadata: Mapped[Optional[Any]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    attachment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    application_id: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)
    raw_payload: Mapped[Optional[Any]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    case: Mapped[Optional["Case"]] = relationship("Case", back_populates="incoming_emails")


class OutgoingEmail(Base):
    __tablename__ = "outgoing_emails"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid, ForeignKey("cases.id", ondelete="SET NULL"), nullable=True, index=True
    )
    application_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    body_plain: Mapped[str] = mapped_column(Text, nullable=False)
    body_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reply_to_message_id: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    correlation_id: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    raw_payload: Mapped[Optional[Any]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    case: Mapped[Optional["Case"]] = relationship("Case", back_populates="outgoing_emails")

