import logging
import secrets
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import authenticate_request
from app.db import get_db
from app.models import Case, IncomingEmail, OutgoingEmail, Payout
from app.schemas.case import (
    CaseCreate,
    CaseDetailResponse,
    CaseDisburseRequest,
    CaseDisburseResponse,
    CaseLinkEmailRequest,
    CaseResponse,
    CaseTimelineItem,
    CaseUpdate,
)
from app.services import ai_service, paypal_service, case_workflow
from app.services.paypal_service import PayPalError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/cases", tags=["cases"])


def _generate_case_number() -> str:
    year = datetime.now().year
    suffix = secrets.token_hex(3).upper()
    return f"CASE-{year}-{suffix}"


def _mask_identifier(val: Optional[str]) -> str:
    if not val:
        return "none"
    if len(val) <= 8:
        return val
    return f"{val[:4]}...{val[-4:]}"


def _find_case_by_identifier(db: Session, identifier: str) -> Optional[Case]:
    """Find a case by UUID or case_number (e.g. CASE-2026-0001)."""
    cleaned = identifier.strip()
    try:
        val_uuid = uuid.UUID(cleaned)
        stmt = select(Case).where(Case.id == val_uuid)
    except ValueError:
        stmt = select(Case).where(func.lower(Case.case_number) == cleaned.lower())

    return db.execute(stmt).scalar_one_or_none()


def _compute_ordered_exchanges(c: Case) -> list[dict[str, str]]:
    """Build or return the ordered list of email exchanges (PK + direction) for a Case."""
    items: list[tuple[datetime, str, str]] = []
    for inc in c.incoming_emails or []:
        ts = inc.received_at
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        items.append((ts, str(inc.id), "incoming"))
    for out in c.outgoing_emails or []:
        ts = out.created_at
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        items.append((ts, str(out.id), "outgoing"))
    items.sort(key=lambda x: x[0])
    computed = [{"id": pk, "direction": direction} for _, pk, direction in items]
    if isinstance(c.email_exchanges, list) and len(c.email_exchanges) >= len(computed):
        return c.email_exchanges
    return computed


def _build_case_response(c: Case) -> CaseResponse:
    inc_count = len(c.incoming_emails) if c.incoming_emails else 0
    out_count = len(c.outgoing_emails) if c.outgoing_emails else 0
    exchanges = _compute_ordered_exchanges(c)
    return CaseResponse(
        id=str(c.id),
        case_number=c.case_number,
        patient_user_id=c.patient_user_id,
        patient_name=c.patient_name,
        patient_email=c.patient_email,
        paypal_email=c.paypal_email,
        medical_category=c.medical_category,
        treatment_description=c.treatment_description,
        hospital_name=c.hospital_name,
        estimated_cost=c.estimated_cost,
        requested_amount=c.requested_amount,
        currency=c.currency,
        urgency=c.urgency,
        status=c.status,
        approval_source=c.approval_source,
        overall_summary=c.overall_summary,
        next_action=c.next_action,
        pending_items=c.pending_items,
        email_exchanges=exchanges,
        incoming_email_count=inc_count,
        outgoing_email_count=out_count,
        created_at=c.created_at,
        updated_at=c.updated_at,
    )


def _build_case_detail_response(c: Case) -> CaseDetailResponse:
    base = _build_case_response(c)
    timeline: list[CaseTimelineItem] = []

    if c.incoming_emails:
        for em in c.incoming_emails:
            body_prev = em.body_plain[:150] if em.body_plain else None
            atts = em.attachment_metadata if isinstance(em.attachment_metadata, list) else None
            timeline.append(
                CaseTimelineItem(
                    id=str(em.id),
                    direction="incoming",
                    message_id=em.message_id,
                    sender=em.sender,
                    recipient=em.recipient,
                    subject=em.subject,
                    body_snippet=body_prev,
                    status="received",
                    timestamp=em.received_at,
                    attachments=atts,
                )
            )

    if c.outgoing_emails:
        for em in c.outgoing_emails:
            body_prev = em.body_plain[:150] if em.body_plain else None
            timeline.append(
                CaseTimelineItem(
                    id=str(em.id),
                    direction="outgoing",
                    message_id=em.reply_to_message_id,
                    sender="Hope Verification",
                    recipient=em.recipient_email,
                    subject=em.subject,
                    body_snippet=body_prev,
                    status=em.status,
                    timestamp=em.created_at,
                    attachments=None,
                )
            )

    # Sort chronological by timestamp (normalizing naive/aware timestamps for safe comparison)
    def _sort_ts(item: CaseTimelineItem) -> datetime:
        ts = item.timestamp
        if ts.tzinfo is None:
            return ts.replace(tzinfo=timezone.utc)
        return ts.astimezone(timezone.utc)

    timeline.sort(key=_sort_ts)

    return CaseDetailResponse(
        **base.model_dump(),
        timeline=timeline,
    )


@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new medical assistance case",
)
def create_case(
    payload: CaseCreate,
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    if not authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing webhook secret.")

    case_num = payload.case_number.strip() if payload.case_number else _generate_case_number()

    # Ensure uniqueness of case_number
    existing = db.execute(select(Case).where(Case.case_number == case_num)).scalar_one_or_none()
    if existing:
        case_num = f"{case_num}-{secrets.token_hex(2).upper()}"

    new_case = Case(
        case_number=case_num,
        patient_user_id=payload.patient_user_id.strip() if payload.patient_user_id else None,
        patient_name=payload.patient_name.strip() if payload.patient_name else None,
        patient_email=payload.patient_email.strip() if payload.patient_email else None,
        paypal_email=payload.paypal_email,
        medical_category=payload.medical_category.strip() if payload.medical_category else None,
        treatment_description=payload.treatment_description,
        hospital_name=payload.hospital_name.strip() if payload.hospital_name else None,
        estimated_cost=payload.estimated_cost,
        requested_amount=payload.requested_amount,
        currency=payload.currency.upper() if payload.currency else "USD",
        urgency=payload.urgency.lower() if payload.urgency else "medium",
        status=payload.status.lower() if payload.status else "new",
        approval_source="reviewer" if payload.status.lower() == "approved" else None,
        overall_summary=payload.overall_summary,
        next_action=payload.next_action,
        pending_items=payload.pending_items,
    )

    try:
        db.add(new_case)
        db.flush()

        # Auto-link any existing unlinked emails matching this case_number
        unlinked_inc = (
            db.execute(
                select(IncomingEmail).where(
                    IncomingEmail.case_id.is_(None),
                    func.lower(IncomingEmail.application_id) == case_num.lower(),
                )
            )
            .scalars()
            .all()
        )
        for inc in unlinked_inc:
            inc.case_id = new_case.id

        unlinked_out = (
            db.execute(
                select(OutgoingEmail).where(
                    OutgoingEmail.case_id.is_(None),
                    func.lower(OutgoingEmail.application_id) == case_num.lower(),
                )
            )
            .scalars()
            .all()
        )
        for out in unlinked_out:
            out.case_id = new_case.id

        db.commit()
        db.refresh(new_case)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error creating case")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create case.")

    payment_reply = case_workflow.process_approved_case(db, new_case)
    if payment_reply:
        case_workflow.notify_case_contact(db, new_case, payment_reply)
    db.commit()

    logger.info("Created new case: id=%s, case_number=%s", new_case.id, new_case.case_number)
    return _build_case_response(new_case)


@router.get(
    "",
    response_model=list[CaseResponse],
    summary="List medical assistance cases with optional filtering",
)
def list_cases(
    request: Request,
    status_filter: Optional[str] = Query(None, alias="status"),
    urgency_filter: Optional[str] = Query(None, alias="urgency"),
    medical_category: Optional[str] = Query(None),
    patient_email: Optional[str] = Query(None),
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    if not authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing webhook secret.")

    stmt = select(Case).order_by(Case.created_at.desc())
    if status_filter:
        stmt = stmt.where(Case.status == status_filter.strip().lower())
    if urgency_filter:
        stmt = stmt.where(Case.urgency == urgency_filter.strip().lower())
    if medical_category:
        stmt = stmt.where(Case.medical_category == medical_category.strip().lower())
    if patient_email:
        stmt = stmt.where(Case.patient_email == patient_email.strip())

    stmt = stmt.offset(offset).limit(limit)
    rows = db.execute(stmt).scalars().all()

    return [_build_case_response(c) for c in rows]


@router.get(
    "/{case_identifier}",
    response_model=CaseDetailResponse,
    summary="Get case details by ID or case_number with full email timeline",
)
def get_case_detail(
    case_identifier: str,
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    if not authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing webhook secret.")

    case_row = _find_case_by_identifier(db, case_identifier)
    if not case_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    return _build_case_detail_response(case_row)


@router.patch(
    "/{case_identifier}",
    response_model=CaseResponse,
    summary="Update case status, summary, next action, or details",
)
def update_case(
    case_identifier: str,
    payload: CaseUpdate,
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    if not authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing webhook secret.")

    case_row = _find_case_by_identifier(db, case_identifier)
    if not case_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    if payload.status is not None:
        case_row.approval_source = 'reviewer' if payload.status.lower() == 'approved' else None

    update_dict = payload.model_dump(exclude_unset=True)
    for field, val in update_dict.items():
        if hasattr(case_row, field):
            setattr(case_row, field, val)

    try:
        db.commit()
        db.refresh(case_row)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error updating case: id=%s", case_row.id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update case.")

    payment_reply = case_workflow.process_approved_case(db, case_row)
    if payment_reply:
        case_workflow.notify_case_contact(db, case_row, payment_reply)
    db.commit()

    logger.info("Updated case id=%s, status=%s", case_row.id, case_row.status)
    return _build_case_response(case_row)


@router.post(
    "/{case_identifier}/link-email",
    response_model=CaseDetailResponse,
    summary="Link an incoming or outgoing email to a case",
)
def link_email_to_case(
    case_identifier: str,
    link_req: CaseLinkEmailRequest,
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    if not authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing webhook secret.")

    case_row = _find_case_by_identifier(db, case_identifier)
    if not case_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    linked_any = False
    if link_req.incoming_email_id:
        try:
            inc_uuid = uuid.UUID(link_req.incoming_email_id.strip())
            inc_email = db.execute(select(IncomingEmail).where(IncomingEmail.id == inc_uuid)).scalar_one_or_none()
            if inc_email:
                inc_email.case_id = case_row.id
                linked_any = True
        except ValueError:
            pass

    if link_req.outgoing_email_id:
        try:
            out_uuid = uuid.UUID(link_req.outgoing_email_id.strip())
            out_email = db.execute(select(OutgoingEmail).where(OutgoingEmail.id == out_uuid)).scalar_one_or_none()
            if out_email:
                out_email.case_id = case_row.id
                linked_any = True
        except ValueError:
            pass

    if not linked_any:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid incoming_email_id or outgoing_email_id found to link.",
        )

    db.flush()
    db.refresh(case_row)
    case_row.email_exchanges = _compute_ordered_exchanges(case_row)
    db.commit()
    db.refresh(case_row)
    return _build_case_detail_response(case_row)


@router.post(
    "/{case_identifier}/disburse",
    response_model=CaseDisburseResponse,
    summary="Disburse PayPal payout to beneficiary for a verified medical case",
)
def disburse_case_payout(
    case_identifier: str,
    request: Request,
    payload: Optional[CaseDisburseRequest] = None,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    secret: Optional[str] = Query(None),
):
    if not authenticate_request(
        request=request,
        header_secret=x_webhook_secret,
        auth_header=authorization,
        query_secret=secret,
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing webhook secret.")

    case_row = _find_case_by_identifier(db, case_identifier)
    if not case_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    if case_row.status not in {'approved', 'payout_processing', 'disbursed', 'paid'}:
        raise HTTPException(status_code=409, detail="Only approved cases can receive payouts.")
    existing = db.execute(select(Payout).where(Payout.case_id == case_row.id)).scalar_one_or_none()
    if payload and existing is None:
        if payload.recipient_email:
            email = case_workflow.extract_paypal_email(f"PayPal: {payload.recipient_email}")
            if not email:
                raise HTTPException(status_code=400, detail="A valid beneficiary PayPal email is required.")
            case_row.paypal_email = email
        if payload.amount is not None:
            case_row.requested_amount = payload.amount
    message = case_workflow.process_approved_case(db, case_row)
    db.commit()
    payout = db.execute(select(Payout).where(Payout.case_id == case_row.id)).scalar_one_or_none()
    if payout is None:
        raise HTTPException(status_code=400, detail=message)
    if payout.batch_status == 'REQUESTED':
        raise HTTPException(status_code=502, detail=message)
    return CaseDisburseResponse(
        case_id=str(case_row.id), case_number=case_row.case_number,
        case_status=case_row.status, batch_id=payout.paypal_batch_id,
        batch_status=payout.batch_status, item_status=payout.item_status,
        amount=f"{payout.amount:.2f}", currency=payout.currency,
        recipient_email=payout.recipient_email,
        paid=payout.item_status == 'SUCCESS', message=message,
    )
