import re
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

MAX_PAYOUT = Decimal("100.00")  # low cap: this page is for Sandbox testing
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class PayoutRequest(BaseModel):
    beneficiary_name: str
    email: str
    amount: str = "1.00"

    @field_validator("beneficiary_name")
    @classmethod
    def validate_name(cls, v):
        v = v.strip()
        if not v or len(v) > 100:
            raise ValueError("Beneficiary name is required (max 100 characters)")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        v = v.strip()
        if len(v) > 127 or not EMAIL_RE.match(v):
            raise ValueError("Enter a valid PayPal recipient email")
        return v

    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(cls, v):
        try:
            value = Decimal(str(v).strip())
        except (InvalidOperation, ValueError):
            raise ValueError("Amount must be a number")
        if not value.is_finite() or value <= 0:
            raise ValueError("Amount must be greater than zero")
        if value != value.quantize(Decimal("0.01")):
            raise ValueError("Amount can have at most 2 decimal places")
        if value > MAX_PAYOUT:
            raise ValueError(f"Amount cannot exceed {MAX_PAYOUT} for sandbox testing")
        return f"{value:.2f}"


class PayoutResponse(BaseModel):
    batch_id: str
    batch_status: str
    item_status: Optional[str] = None
    item_id: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    final: bool
    paid: bool
    message: str
    error: Optional[str] = None


class PayoutRecord(BaseModel):
    """A persisted payout (database row)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    beneficiary_name: Optional[str] = None
    recipient_email: str
    amount: Decimal
    currency: str
    payment_provider: str
    paypal_batch_id: str
    paypal_item_id: Optional[str] = None
    paypal_transaction_id: Optional[str] = None
    batch_status: str
    item_status: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PayoutHistoryResponse(BaseModel):
    count: int
    limit: int
    offset: int
    items: list[PayoutRecord]
