import logging
import re
import uuid
from decimal import Decimal
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.routes.auth import require_admin_session
from app.db import get_db
from app.models import Payout
from app.schemas.payout import PayoutHistoryResponse, PayoutRecord, PayoutRequest, PayoutResponse
from app.services import paypal_service
from app.services.paypal_service import PayPalError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/payouts", tags=["payouts"])

BATCH_ID_RE = re.compile(r"^[A-Za-z0-9\-]{5,64}$")

# Item statuses after which PayPal will not change its mind on its own.
FINAL_ITEM_STATUSES = {"SUCCESS", "FAILED", "RETURNED", "BLOCKED", "REFUNDED", "REVERSED", "UNCLAIMED"}
FINAL_BATCH_FAILURES = {"DENIED", "CANCELED"}


def _summarise(data: dict) -> PayoutResponse:
    header = data.get("batch_header", {})
    batch_id = header.get("payout_batch_id", "")
    batch_status = header.get("batch_status", "UNKNOWN")

    items = data.get("items") or []
    item = items[0] if items else None
    item_status = item.get("transaction_status") if item else None
    item_error = (item.get("errors") or {}).get("message") if item else None

    # "Paid" only when PayPal confirms the ITEM status is SUCCESS.
    paid = item_status == "SUCCESS"
    final = item_status in FINAL_ITEM_STATUSES or batch_status in FINAL_BATCH_FAILURES

    if paid:
        message = "Payout completed. PayPal confirmed the item as SUCCESS."
    elif item_status == "UNCLAIMED":
        message = "Recipient has no PayPal account yet; funds are unclaimed."
    elif final:
        message = f"Payout did not complete (item: {item_status or batch_status})."
    elif item_status is None:
        message = f"Batch {batch_status}. Waiting for PayPal to process the item."
    else:
        message = f"Payout in progress (item: {item_status})."

    amount = (item.get("payout_item", {}).get("amount") or {}) if item else {}
    return PayoutResponse(
        batch_id=batch_id,
        batch_status=batch_status,
        item_status=item_status,
        item_id=item.get("payout_item_id") if item else None,
        amount=amount.get("value"),
        currency=amount.get("currency"),
        final=final,
        paid=paid,
        message=message,
        error=item_error,
    )


def _persist(db: Session, data: dict, request: PayoutRequest | None = None) -> Payout | None:
    """Insert or update the payouts row for this PayPal batch, copying PayPal's own statuses.

    A row is only created when ``request`` is given (i.e. from create). Status lookups
    for unknown batches return None instead of inventing a record.
    """
    header = data.get("batch_header", {})
    batch_id = header.get("payout_batch_id")
    if not batch_id:
        return None
    items = data.get("items") or []
    item = items[0] if items else {}

    fields = {
        "batch_status": header.get("batch_status"),
        "paypal_item_id": item.get("payout_item_id"),
        "paypal_transaction_id": item.get("transaction_id"),
        "item_status": item.get("transaction_status"),
        "raw_response": data,
    }

    def apply(row: Payout) -> None:
        for key, value in fields.items():
            if value is not None:
                setattr(row, key, value)

    def find() -> Payout | None:
        return db.execute(select(Payout).where(Payout.paypal_batch_id == batch_id)).scalar_one_or_none()

    row = find()
    if row is None and request is None:
        return None
    try:
        if row is None:
            row = Payout(
                beneficiary_name=request.beneficiary_name,
                recipient_email=request.email,
                amount=Decimal(request.amount),
                currency="USD",
                payment_provider="paypal",
                paypal_batch_id=batch_id,
                batch_status=fields["batch_status"] or "PENDING",
            )
            apply(row)
            db.add(row)
        else:
            apply(row)
        db.commit()
    except IntegrityError:
        # A concurrent request already inserted this batch/item: update that row.
        db.rollback()
        row = find()
        if row is None:
            raise
        apply(row)
        db.commit()
    return row


@router.get("/history", response_model=PayoutHistoryResponse)
def payout_history(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _session: dict = Depends(require_admin_session),
):
    try:
        total = db.execute(select(func.count()).select_from(Payout)).scalar_one()
        rows = db.execute(
            select(Payout).order_by(Payout.created_at.desc(), Payout.id).limit(limit).offset(offset)
        ).scalars().all()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error. Please try again.")
    return PayoutHistoryResponse(
        count=total, limit=limit, offset=offset, items=[PayoutRecord.model_validate(r) for r in rows]
    )


@router.post("/create", response_model=PayoutResponse)
def create_payout(body: PayoutRequest, db: Session = Depends(get_db)):
    try:
        created = paypal_service.create_payout(
            body.email, body.amount, f"Hope payout to {body.beneficiary_name}"
        )
    except PayPalError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    batch_id = created.get("batch_header", {}).get("payout_batch_id")
    if not batch_id:
        raise HTTPException(status_code=502, detail="PayPal did not return a payout batch ID")

    # Read the batch back so the response (and saved record) reflect PayPal's actual state.
    try:
        data = paypal_service.get_payout(batch_id)
    except PayPalError:
        data = created

    try:
        _persist(db, data, request=body)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Could not persist payout batch %s", batch_id)
        raise HTTPException(
            status_code=500,
            detail="Payout was sent to PayPal but could not be recorded. Batch ID: " + batch_id,
        )
    return _summarise(data)


@router.get("/{identifier}", response_model=Union[PayoutRecord, PayoutResponse])
def payout_lookup(identifier: str, db: Session = Depends(get_db)):
    """A database UUID returns the saved record; a PayPal batch ID checks (and syncs) PayPal."""
    try:
        record_id = uuid.UUID(identifier)
    except ValueError:
        record_id = None

    if record_id is not None:
        try:
            row = db.get(Payout, record_id)
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error. Please try again.")
        if row is None:
            raise HTTPException(status_code=404, detail="Payout record not found")
        return PayoutRecord.model_validate(row)

    if not BATCH_ID_RE.match(identifier):
        raise HTTPException(status_code=400, detail="Invalid batch ID")
    try:
        data = paypal_service.get_payout(identifier)
    except PayPalError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    try:
        _persist(db, data)
    except SQLAlchemyError:
        # The status check must still work if the sync fails; the next poll retries.
        db.rollback()
        logger.exception("Could not update payout batch %s", identifier)
    return _summarise(data)
