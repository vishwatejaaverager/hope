"""Document records and immutable review snapshots for continued case conversations."""
from sqlalchemy import select
from app.models import CaseDocument, CaseReview, IncomingEmail, OutgoingEmail
from app.services.approval_policy import _source
from app.services.case_review import document_verified
from app.services.attachment_service import normalize


def register_documents(db, email, attachments):
    records = []
    for index, attachment in enumerate(attachments):
        doc = db.execute(select(CaseDocument).where(
            CaseDocument.email_id == email.id, CaseDocument.attachment_index == index)).scalar_one_or_none()
        if doc is None:
            doc = CaseDocument(email_id=email.id, case_id=email.case_id, attachment_index=index,
                               source_id=_source(attachment), filename=str(attachment.get('filename') or 'Document'),
                               file_metadata=attachment, document_type='other', status='pending', is_current=True)
            db.add(doc)
        records.append(doc)
    db.flush()
    return records


def backfill_case(db, case):
    """Materialize legacy email metadata without inventing verification results."""
    evidence = {item.get('source_id'): item for item in (case.verification_evidence or []) if isinstance(item, dict)}
    emails = db.execute(select(IncomingEmail).where(IncomingEmail.case_id == case.id)
                        .order_by(IncomingEmail.received_at, IncomingEmail.id)).scalars().all()
    for email in emails:
        documents = register_documents(db, email, normalize(email.attachment_metadata))
        for doc in documents:
            old = evidence.get(doc.source_id)
            if doc.status == 'pending' and old:
                doc.document_type = str(old.get('document_type') or 'other')
                doc.extracted_data = old
                doc.status = 'verified' if document_verified(old) else 'needs_review'
                doc.reason = old.get('reason')
        snapshot = (email.raw_payload or {}).get('review_report')
        if snapshot and not db.execute(select(CaseReview.id).where(CaseReview.email_id == email.id)).first():
            db.add(CaseReview(case_id=case.id, email_id=email.id, report=snapshot))
    db.flush()
    # Superseded historical files remain available but cannot satisfy current requirements.
    current_sources = set(evidence)
    for doc in db.execute(select(CaseDocument).where(CaseDocument.case_id == case.id)).scalars():
        if doc.status != 'pending':
            doc.is_current = doc.source_id in current_sources


def context(db, case, current_email_id=None):
    docs = db.execute(select(CaseDocument).where(CaseDocument.case_id == case.id)
                      .order_by(CaseDocument.created_at, CaseDocument.id)).scalars().all()
    recent = []
    for row in db.execute(select(IncomingEmail).where(IncomingEmail.case_id == case.id, IncomingEmail.id != current_email_id)
                          .order_by(IncomingEmail.received_at.desc()).limit(6)).scalars():
        recent.append({'direction': 'incoming', 'at': row.received_at.isoformat(), 'body': (row.body_plain or '')[:4000]})
    for row in db.execute(select(OutgoingEmail).where(OutgoingEmail.case_id == case.id)
                          .order_by(OutgoingEmail.created_at.desc()).limit(6)).scalars():
        recent.append({'direction': 'outgoing', 'at': row.created_at.isoformat(), 'body': row.body_plain[:4000]})
    recent.sort(key=lambda row: row['at'])
    return {'documents': [serialize_document(doc) for doc in docs if doc.email_id != current_email_id], 'recent_messages': recent}


def save_review(db, case, email, documents, analysis):
    report = analysis.get('review_report')
    for doc in documents:
        doc.case_id = case.id
    if not report:
        for doc in documents:
            doc.status = 'analysis_failed' if analysis.get('analysis_status') == 'failed' else 'pending'
        if analysis.get('analysis_status') == 'failed':
            db.add(CaseReview(case_id=case.id, email_id=email.id, report={
                'analysis_status': 'failed', 'failure_reason': analysis.get('failure_reason')},
                reply_draft=analysis.get('auto_reply_body')))
        return
    evidence = {item.get('source_id'): item for item in analysis.get('verification_evidence', [])}
    for doc in db.execute(select(CaseDocument).where(CaseDocument.case_id == case.id)).scalars():
        item = evidence.get(doc.source_id)
        doc.is_current = item is not None
        if item:
            doc.document_type = str(item.get('document_type') or 'other')
            doc.extracted_data = item
            doc.status = 'verified' if document_verified(item) else 'needs_review'
            doc.reason = str(item.get('reason') or 'Document verification is incomplete.')
    snapshot = CaseReview(case_id=case.id, email_id=email.id, report=report,
                          reply_draft=analysis.get('auto_reply_body'))
    db.add(snapshot)
    return snapshot


def serialize_document(doc):
    return {'id': str(doc.id), 'email_id': str(doc.email_id), 'source_id': doc.source_id,
            'filename': doc.filename, 'document_type': doc.document_type, 'status': doc.status,
            'is_current': doc.is_current, 'reason': doc.reason, 'data': doc.extracted_data,
            'file': doc.file_metadata}


def case_context(db, case, current_email_id=None):
    return {
        **context(db, case, current_email_id),
        "case_number": case.case_number,
        "patient_name": case.patient_name,
        "patient_email": case.patient_email,
        "paypal_email": case.paypal_email,
        "verification_evidence": case.verification_evidence,
        "verification_issues": case.verification_issues,
        "review_report": case.review_report,
        "medical_category": case.medical_category,
        "hospital_name": case.hospital_name,
        "estimated_cost": str(case.estimated_cost) if case.estimated_cost else None,
        "requested_amount": str(case.requested_amount) if case.requested_amount else None,
        "urgency": case.urgency,
        "status": case.status,
        "overall_summary": case.overall_summary,
        "next_action": case.next_action,
        "pending_items": case.pending_items,
    }

def load_case_preview(case_number):
    """Load an existing case for local testing without updating its records."""
    from sqlalchemy import func, text
    from app.db import SessionLocal
    from app.models import Case

    with SessionLocal() as db:
        if db.get_bind().dialect.name == 'postgresql':
            db.execute(text('SET TRANSACTION READ ONLY'))
        case = db.execute(select(Case).where(
            func.lower(Case.case_number) == case_number.strip().lower()
        )).scalar_one_or_none()
        return case_context(db, case) if case is not None else None
