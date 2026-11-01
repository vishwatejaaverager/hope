from decimal import Decimal, InvalidOperation
from typing import Optional

from pydantic import BaseModel, field_validator

SUPPORTED_CURRENCIES = {"USD"}  # Sandbox testing; INR returned CURRENCY_NOT_SUPPORTED
MIN_AMOUNT = Decimal("1.00")
MAX_AMOUNT = Decimal("10000.00")


class CreateOrderRequest(BaseModel):
    amount: str
    currency: str = "USD"

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
        if value < MIN_AMOUNT or value > MAX_AMOUNT:
            raise ValueError(f"Amount must be between {MIN_AMOUNT} and {MAX_AMOUNT}")
        return f"{value:.2f}"

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v):
        v = v.upper()
        if v not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency. Supported: {', '.join(sorted(SUPPORTED_CURRENCIES))}")
        return v


class CreateOrderResponse(BaseModel):
    order_id: str
    status: str


class CaptureOrderResponse(BaseModel):
    order_id: str
    order_status: str
    capture_status: Optional[str] = None
    transaction_id: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    success: bool
    message: str
