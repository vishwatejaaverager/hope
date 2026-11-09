from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    model_config = ConfigDict(extra="allow")

    case_number: Optional[str] = Field(None, max_length=32, description="Optional custom case ID (auto-generated if omitted)")
    patient_user_id: Optional[str] = Field(None, max_length=64)
    patient_name: Optional[str] = Field(None, max_length=255)
    paypal_email: Optional[str] = Field(None, max_length=255, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    patient_email: Optional[str] = Field(None, max_length=255)
    medical_category: Optional[str] = Field(None, max_length=64, description="e.g. upcoming_surgery, ongoing_hospitalization")
    treatment_description: Optional[str] = None
    hospital_name: Optional[str] = Field(None, max_length=255)
    estimated_cost: Optional[Decimal] = None
    requested_amount: Optional[Decimal] = None
    currency: str = Field("USD", max_length=3)
    urgency: str = Field("medium", max_length=32, description="low, medium, high, critical")
    status: str = Field("new", max_length=32, description="new, awaiting_documents, under_review, approved, rejected, closed")
    overall_summary: Optional[str] = None
    next_action: Optional[str] = Field(None, max_length=255)
    pending_items: Optional[Union[list[Any], dict[str, Any]]] = None
    email_exchanges: Optional[list[Any]] = None


class CaseUpdate(BaseModel):
    model_config = ConfigDict(extra="allow")

    patient_name: Optional[str] = Field(None, max_length=255)
    paypal_email: Optional[str] = Field(None, max_length=255, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    patient_email: Optional[str] = Field(None, max_length=255)
    medical_category: Optional[str] = Field(None, max_length=64)
    treatment_description: Optional[str] = None
    hospital_name: Optional[str] = Field(None, max_length=255)
    estimated_cost: Optional[Decimal] = None
    requested_amount: Optional[Decimal] = None
    currency: Optional[str] = Field(None, max_length=3)
    urgency: Optional[str] = Field(None, max_length=32)
    status: Optional[str] = Field(None, max_length=32)
    overall_summary: Optional[str] = None
    next_action: Optional[str] = Field(None, max_length=255)
    pending_items: Optional[Union[list[Any], dict[str, Any]]] = None
    email_exchanges: Optional[list[Any]] = None


class CaseResponse(BaseModel):
    id: str
    case_number: str
    patient_user_id: Optional[str] = None
    patient_name: Optional[str] = None
    paypal_email: Optional[str] = Field(None, max_length=255, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    patient_email: Optional[str] = None
    medical_category: Optional[str] = None
    treatment_description: Optional[str] = None
    hospital_name: Optional[str] = None
    estimated_cost: Optional[Decimal] = None
    requested_amount: Optional[Decimal] = None
    currency: str
    urgency: str
    status: str
    overall_summary: Optional[str] = None
    next_action: Optional[str] = None
    pending_items: Optional[Any] = None
    email_exchanges: list[Any] = []
    incoming_email_count: int = 0
    outgoing_email_count: int = 0
    created_at: datetime
    updated_at: datetime


class CaseTimelineItem(BaseModel):
    id: str
    direction: str  # "incoming" or "outgoing"
    message_id: Optional[str] = None
    sender: Optional[str] = None
    recipient: Optional[str] = None
    subject: Optional[str] = None
    body_snippet: Optional[str] = None
    status: Optional[str] = None
    timestamp: datetime
    attachments: Optional[list[dict[str, Any]]] = None


class CaseDetailResponse(CaseResponse):
    timeline: list[CaseTimelineItem] = []


class CaseLinkEmailRequest(BaseModel):
    incoming_email_id: Optional[str] = None
    outgoing_email_id: Optional[str] = None


class CaseDisburseRequest(BaseModel):
    recipient_email: Optional[str] = Field(None, description="Override recipient PayPal email (defaults to the confirmed case.paypal_email)")
    amount: Optional[Decimal] = Field(None, description="Override payout amount in USD (defaults to requested_amount or estimated_cost)")
    beneficiary_name: Optional[str] = Field(None, description="Override beneficiary name (defaults to case.patient_name)")


class CaseDisburseResponse(BaseModel):
    case_id: str
    case_number: str
    case_status: str
    batch_id: str
    batch_status: str
    item_status: Optional[str] = None
    amount: str
    currency: str = "USD"
    recipient_email: str
    paid: bool = False
    message: str

