"""Check pending PayPal batches and notify applicants once a payout succeeds."""
import logging
import threading
from time import sleep

from sqlalchemy import select

from app.db import SessionLocal
from app.models import Case, Payout
from app.services import case_workflow, paypal_service

logger = logging.getLogger(__name__)
_started = False
_TERMINAL_ITEMS = {'SUCCESS', 'FAILED', 'RETURNED', 'BLOCKED', 'REFUNDED', 'REVERSED'}


def reconcile_pending(db):
    ids = db.execute(
        select(Case.id).join(Payout, Payout.case_id == Case.id)
        .where(Case.status == 'payout_processing', Payout.batch_status != 'REQUESTED',
               Payout.batch_status.not_in({'DENIED', 'CANCELED'}),
               (Payout.item_status.is_(None) | Payout.item_status.not_in(_TERMINAL_ITEMS)))
        .order_by(Payout.updated_at).limit(20)
    ).scalars().all()
    for case_id in ids:
        try:
            case = db.execute(select(Case).where(Case.id == case_id, Case.status == 'payout_processing')
                              .with_for_update(skip_locked=True).execution_options(populate_existing=True)).scalar_one_or_none()
            if case is not None:
                case_workflow.process_approved_case(db, case, notify_on_success=True)
            db.commit()
        except Exception:
            db.rollback()
            logger.exception('Could not reconcile pending payout')


def start_poller():
    global _started
    if _started or not paypal_service.CLIENT_ID or not paypal_service.CLIENT_SECRET:
        return
    _started = True

    def poll():
        while True:
            sleep(60)
            try:
                with SessionLocal() as db:
                    reconcile_pending(db)
            except Exception:
                logger.exception('Could not check pending payouts')

    threading.Thread(target=poll, name='hope-payout-reconciliation', daemon=True).start()
