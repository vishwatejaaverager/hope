"""Approval, confirmed beneficiary details, and idempotent case payouts."""
import re
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Case, Payout
from app.services import paypal_service, approval_policy, case_review
from app.services.paypal_service import PayPalError

EMAIL_RE = r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+"


def extract_paypal_email(body: str | None, awaiting_email: bool = False) -> str | None:
    # Ignore quoted history and signatures; never infer PayPal ownership from From.
    text = re.split(r"(?m)^On .+wrote:|^-----Original Message-----|^--\s*$", body or '')[0]
    text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('>'))
    addresses = re.findall(EMAIL_RE, text)
    if len(set(addresses)) != 1:
        return None
    labelled = re.search(
        rf"\bpaypal(?:\s+account)?(?:\s+(?:e-?mail(?:\s+address)?|address))?\s*(?::|is|=)\s*<?({EMAIL_RE})",
        text, re.I,
    )
    if labelled and not re.search(r"\b(?:not|isn't|is not|don't|do not)\b", text[:labelled.start()], re.I):
        return labelled.group(1)
    if awaiting_email and text.strip().strip('<> .') == addresses[0]:
        return addresses[0]
    return None


def process_approved_case(db: Session, case: Case) -> str | None:
    """Return factual payment instructions; persist intent before contacting PayPal.

    A unique case linkage and stable PayPal request ID make webhook/admin retries
    reuse the same payout, including after a timeout or database failure.
    """
    if case.status not in {'approved', 'payout_processing', 'disbursed', 'paid'}:
        return None
    db.flush()
    db.execute(select(Case).where(Case.id == case.id).with_for_update()).scalar_one()
    payout = db.execute(select(Payout).where(Payout.case_id == case.id)).scalar_one_or_none()
    if payout is None:
        if case.status in {'disbursed', 'paid'}:
            return 'This case is already marked as paid. Our team will review its existing payment record before taking any further action.'
        if case.approval_source == case_review.APPROVAL_SOURCE and not case_review.authorizes_payment(case.review_report):
            case.status = 'under_review'
            case.approval_source = None
            case.next_action = 'Complete the case review and resolve red flags before payment'
            return 'Your case needs further review before payment can be arranged.'
        if case.approval_source == approval_policy.DOCUMENT_CHECKS:
            date_issues = approval_policy.validity_issues(case.verification_evidence or [])
            if date_issues:
                case.status = 'under_review'
                case.approval_source = None
                case.verification_issues = list(dict.fromkeys([*(case.verification_issues or []), *date_issues]))
                case.next_action = 'Obtain current documents and recheck validity before payment'
                return 'Your application requires an updated document validity check before payment can be arranged. Please provide current supporting documents for review.'
        if (case.approval_source not in approval_policy.TRUSTED_APPROVALS
                or (case.approval_source == approval_policy.DOCUMENT_CHECKS and (
                    case.verification_issues or
                    {item.get('document_type') for item in (case.verification_evidence or [])} != set(approval_policy.REQUIRED)
                ))):
            case.status = 'under_review'
            case.next_action = 'Verify supporting documents before authorizing payment'
            return approval_policy.REVIEW_MESSAGE
        if not case.paypal_email:
            case.next_action = 'Request beneficiary PayPal email'
            return 'Your case is approved. Please reply with the email address registered to the beneficiary’s PayPal account so we can send the approved assistance. Your contact email may be different.'
        amount = case.requested_amount
        if amount is None or not amount.is_finite() or amount <= 0 or amount != amount.quantize(Decimal('0.01')):
            case.next_action = 'Confirm approved payout amount in USD'
            return 'Your case is approved and we have your PayPal email. Our team still needs to confirm the approved assistance amount before sending payment.'
        if case.currency != 'USD':
            case.next_action = 'Review payout currency; only USD is supported'
            return 'Your case is approved. Our team needs to confirm the payout currency before sending payment.'
        payout = Payout(case_id=case.id, beneficiary_name=case.patient_name,
                        recipient_email=case.paypal_email, amount=amount, currency=case.currency,
                        paypal_batch_id=f'REQUEST-{case.id.hex}', batch_status='REQUESTED')
        db.add(payout)
        case.status = 'payout_processing'
        case.next_action = 'Submit approved payout to PayPal'
        db.commit()  # Freeze recipient and amount before any external side effect.
    try:
        if payout.batch_status == 'REQUESTED':
            data = paypal_service.create_payout(
                payout.recipient_email, f'{payout.amount:.2f}',
                f'Hope medical assistance for {case.case_number}',
                currency=payout.currency, request_id=f'HOPE-CASE-{case.id.hex}',
            )
            batch_id = data.get('batch_header', {}).get('payout_batch_id')
            if not batch_id:
                raise PayPalError('PayPal did not return a payout batch ID', 502)
            payout.paypal_batch_id = batch_id
            payout.batch_status = data.get('batch_header', {}).get('batch_status', 'PENDING')
            payout.raw_response = data
            db.commit()  # Record accepted batch before polling.
        data = paypal_service.get_payout(payout.paypal_batch_id)
        item = (data.get('items') or [{}])[0]
        payout.batch_status = data.get('batch_header', {}).get('batch_status', payout.batch_status)
        payout.item_status = item.get('transaction_status')
        payout.paypal_item_id = item.get('payout_item_id')
        payout.paypal_transaction_id = item.get('transaction_id')
        payout.raw_response = data
    except PayPalError:
        case.next_action = 'Reconcile payout with PayPal; retry with the same case request ID'
        db.commit()
        return 'Your case is approved, but we could not confirm the payout status with PayPal. Our team will check it before confirming payment; you do not need to resubmit your documents.'

    if payout.item_status == 'SUCCESS':
        case.status = 'disbursed'
        case.next_action = 'Payout confirmed successful by PayPal'
        message = f'PayPal has confirmed your payment of ${payout.amount:.2f} USD to {payout.recipient_email}. Reference: {payout.paypal_batch_id}.'
    elif payout.item_status in {'FAILED', 'RETURNED', 'BLOCKED', 'REFUNDED', 'REVERSED', 'UNCLAIMED'} or payout.batch_status in {'DENIED', 'CANCELED'}:
        case.status = 'payout_processing'
        case.next_action = f'Review unsuccessful PayPal payout: {payout.item_status or payout.batch_status}'
        message = f'PayPal has not completed your ${payout.amount:.2f} USD payout (status: {payout.item_status or payout.batch_status}). Our team will review this payment; please do not submit another application. Reference: {payout.paypal_batch_id}.'
    else:
        case.status = 'payout_processing'
        case.next_action = f'Check PayPal payout status: {payout.item_status or payout.batch_status}'
        message = f'Your approved assistance of ${payout.amount:.2f} USD has been submitted to PayPal for {payout.recipient_email}. Its current status is {payout.item_status or payout.batch_status}; payment completion is not yet confirmed. Reference: {payout.paypal_batch_id}.'
    db.commit()
    return message


def notify_case_contact(db: Session, case: Case, message: str) -> None:
    """Persist approval updates, then use the configured email transport."""
    import os
    import requests
    from app.models import OutgoingEmail
    from app.services import smtp_service

    if not case.patient_email:
        return
    email = OutgoingEmail(
        case_id=case.id, application_id=case.case_number,
        recipient_email=case.patient_email,
        subject=f'Update on your Hope application [{case.case_number}]',
        body_plain=f"Hi {case.patient_name or 'there'},\n\n{message}\n\nWarm regards,\nHope Medical Team",
        status='pending',
    )
    db.add(email)
    db.commit()
    if smtp_service.send_threaded_email(email.recipient_email, email.subject, email.body_plain):
        email.status = 'sent'
        db.commit()
    elif os.getenv('ZAPIER_OUTBOUND_WEBHOOK_URL'):
        try:
            response = requests.post(os.environ['ZAPIER_OUTBOUND_WEBHOOK_URL'], json={
                'email_id': str(email.id), 'application_id': email.application_id,
                'to': email.recipient_email, 'recipient_email': email.recipient_email,
                'subject': email.subject, 'body': email.body_plain,
            }, timeout=5)
            response.raise_for_status()
        except requests.RequestException:
            # Keep the persisted email pending for the existing dispatch queue.
            pass
