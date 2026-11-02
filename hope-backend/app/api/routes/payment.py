import re
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Donation
from app.schemas.payment import (
    CaptureOrderResponse,
    CreateOrderRequest,
    CreateOrderResponse,
    DonationHistoryResponse,
    DonationRecord,
)
from app.services import paypal_service
from app.services.paypal_service import PayPalError

router = APIRouter(prefix="/api/payments", tags=["payments"])

ORDER_ID_RE = re.compile(r"^[A-Za-z0-9\-]{5,64}$")


@router.get("/config")
def config():
    """Public PayPal client ID (safe to expose; the secret never leaves the server)."""
    try:
        return {"client_id": paypal_service.get_client_id(), "currency": "USD"}
    except PayPalError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/history", response_model=DonationHistoryResponse)
def donation_history(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    try:
        total = db.execute(select(func.count()).select_from(Donation)).scalar_one()
        rows = db.execute(
            select(Donation).order_by(Donation.created_at.desc(), Donation.id.desc()).limit(limit).offset(offset)
        ).scalars().all()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error. Please try again.")
    return DonationHistoryResponse(
        count=total,
        limit=limit,
        offset=offset,
        items=[DonationRecord.model_validate(r) for r in rows],
    )


@router.post("/create-order", response_model=CreateOrderResponse)
def create_order(body: CreateOrderRequest, db: Session = Depends(get_db)):
    try:
        order = paypal_service.create_order(body.amount, body.currency)
    except PayPalError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    # Nothing is saved yet: a donation is recorded only after PayPal captures it.
    return CreateOrderResponse(order_id=order["id"], status=order["status"])


def _map_status(order_status: str, capture_status: str | None) -> str:
    """Translate PayPal's reported state into our payment_status."""
    if order_status == "COMPLETED" and capture_status == "COMPLETED":
        return "COMPLETED"
    if capture_status in ("PENDING", "REFUNDED", "PARTIALLY_REFUNDED"):
        return capture_status
    if capture_status in ("DECLINED", "FAILED"):
        return "FAILED"
    return "CREATED" if order_status in ("CREATED", "APPROVED", "PAYER_ACTION_REQUIRED") else order_status


@router.post("/capture-order/{order_id}", response_model=CaptureOrderResponse)
def capture_order(order_id: str, db: Session = Depends(get_db)):
    if not ORDER_ID_RE.match(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID")

    try:
        donation = db.execute(
            select(Donation).where(Donation.paypal_order_id == order_id)
        ).scalar_one_or_none()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error. Please try again.")

    # Already captured and recorded: don't touch PayPal again.
    if donation is not None and donation.payment_status == "COMPLETED":
        db.rollback()
        return CaptureOrderResponse(
            order_id=order_id,
            order_status="COMPLETED",
            capture_status="COMPLETED",
            transaction_id=donation.paypal_capture_id,
            amount=f"{donation.amount:.2f}",
            currency=donation.currency,
            success=True,
            message="Payment completed. Thank you for your donation!",
        )

    try:
        result = paypal_service.capture_order(order_id)
    except PayPalError as exc:
        db.rollback()
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    order_status = result.get("status", "UNKNOWN")
    capture = None
    try:
        captures = result["purchase_units"][0]["payments"]["captures"]
        capture = captures[0] if captures else None
    except (KeyError, IndexError):
        pass

    capture_status = capture.get("status") if capture else None
    # Success ONLY if PayPal reports the capture itself as COMPLETED.
    success = order_status == "COMPLETED" and capture_status == "COMPLETED"

    if success:
        message = "Payment completed. Thank you for your donation!"
    elif capture_status == "PENDING":
        message = "Payment is pending review by PayPal."
    else:
        message = f"Payment not completed (order: {order_status}, capture: {capture_status})."

    amount = capture.get("amount", {}) if capture else {}

    # Persist exactly what PayPal reported (only if a capture exists to record).
    if capture:
        payer = result.get("payer") or {}
        name = payer.get("name") or {}
        full_name = " ".join(p for p in (name.get("given_name"), name.get("surname")) if p) or None
        fields = {
            "payment_status": _map_status(order_status, capture_status),
            "paypal_capture_id": capture.get("id"),
            "amount": Decimal(amount["value"]) if amount.get("value") else None,
            "currency": amount.get("currency_code"),
            "donor_name": full_name,
            "donor_email": payer.get("email_address"),
        }

        def apply(row: Donation) -> None:
            for key, value in fields.items():
                if value is not None:
                    setattr(row, key, value)

        try:
            if donation is None:
                donation = Donation(paypal_order_id=order_id, payment_provider="paypal")
                apply(donation)
                db.add(donation)
            else:
                apply(donation)
            db.commit()
        except IntegrityError:
            # Concurrent duplicate request already inserted it: update that row instead.
            db.rollback()
            try:
                row = db.execute(
                    select(Donation).where(Donation.paypal_order_id == order_id)
                ).scalar_one()
                apply(row)
                db.commit()
            except SQLAlchemyError:
                db.rollback()
                raise HTTPException(
                    status_code=500,
                    detail="Payment was processed by PayPal but could not be recorded. Contact support with order " + order_id,
                )
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Payment was processed by PayPal but could not be recorded. Contact support with order " + order_id,
            )

    return CaptureOrderResponse(
        order_id=result.get("id", order_id),
        order_status=order_status,
        capture_status=capture_status,
        transaction_id=capture.get("id") if capture else None,
        amount=amount.get("value"),
        currency=amount.get("currency_code"),
        success=success,
        message=message,
    )
