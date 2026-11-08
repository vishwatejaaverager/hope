from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    model_config = ConfigDict(extra="allow")

    case_number: Optional[str] = Field(None, max_length=32, description="Optional custom case ID (auto-generated if omitted)")
    patient_user_id: Optional[str] = Field(None, max_length=64)
    patient_name: Optional[str] = Field(None, max_length=255)
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


class CaseUpdate(BaseModel):
    model_config = ConfigDict(extra="allow")

    patient_name: Optional[str] = Field(None, max_length=255)
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


class CaseResponse(BaseModel):
    id: str
    case_number: str
    patient_user_id: Optional[str] = None
    patient_name: Optional[str] = None
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
    ai_summary: Optional[Any] = None


class CaseDetailResponse(CaseResponse):
    timeline: list[CaseTimelineItem] = []


class CaseLinkEmailRequest(BaseModel):
    incoming_email_id: Optional[str] = None
    outgoing_email_id: Optional[str] = None
