"""Evidence-based case approval. AI confidence alone cannot authorize a payout."""
import hashlib
import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

REVIEWER = 'reviewer'
DOCUMENT_CHECKS = 'document_checks'
TRUSTED_APPROVALS = {REVIEWER, DOCUMENT_CHECKS}
REQUIRED = {
    'medical_record': 'a medical prescription or consultation report',
    'cost_estimate': 'the hospital treatment cost estimate or bill',
    'government_id': 'the patient’s government identification document',
}
REVIEW_MESSAGE = 'Your application remains under review. Its earlier approval needs to be rechecked against the supporting documents before payment can be arranged.'


def _name(value: Any) -> str:
    return re.sub(r'[^a-z0-9]', '', re.sub(r'\b(?:mrs|mr|ms|dr)\.?(?:\s+|$)', '', str(value or '').lower()))


def _source(attachment: dict) -> str:
    return hashlib.sha256(json.dumps(attachment, sort_keys=True, default=str).encode()).hexdigest()


def constrain_email_analysis(analysis: dict[str, Any], sender: str, subject: str | None,
                             body: str | None, attachments: list[dict[str, Any]],
                             existing_evidence: list | None = None, existing_issues: list | None = None) -> dict[str, Any]:
    from app.services.ai_service import _extract_image_urls

    result = dict(analysis)
    inspected_image_urls = set(_extract_image_urls(attachments)[:4])
    # Previous evidence comes only from a server-owned Case column, never from
    # a summary or model-provided history.
    evidence = {item['document_type']: dict(item) for item in (existing_evidence or [])
                if isinstance(item, dict) and item.get('document_type') in REQUIRED}
    checks = result.get('document_checks')
    checks = checks if isinstance(checks, list) else []
    issues = result.get('verification_issues')
    issues = list(map(str, issues)) if isinstance(issues, list) else []
    def absent_document_notice(issue: str) -> bool:
        lowered = issue.lower()
        return (lowered.startswith('missing ') and
                any(label in lowered for label in ('cost estimate', 'government-issued identification',
                    'government identification', 'government id', 'medical record', 'medical report')) and
                not any(detail in lowered for detail in ('signature', 'stamp', 'date', 'amount', 'name', 'alteration')))
    # Required-document absence is recomputed below. Do not persist it as an
    # authenticity warning that survives after the missing file is supplied.
    issues = [issue for issue in issues if not absent_document_notice(issue)]
    existing_issues = [str(issue) for issue in (existing_issues or []) if not absent_document_notice(str(issue))]
    newly_verified = set()
    sources_used = {item.get('source_id'): kind for kind, item in evidence.items()}
    for check in checks:
        if not isinstance(check, dict):
            issues.append('Invalid document verification result')
            continue
        kind, index = check.get('document_type'), check.get('attachment_index')
        if kind not in REQUIRED or type(index) is not int or not 0 <= index < len(attachments):
            issues.append('Document evidence does not identify a supplied attachment')
            continue
        if check.get('verdict') != 'verified':
            evidence.pop(kind, None)
            issues.append(f'{kind} requires further verification')
            continue
        attachment = attachments[index]
        text = str(attachment.get('extracted_text') or '').strip()
        url = str(attachment.get('url') or '')
        is_image = str(attachment.get('content_type') or '').startswith('image/') or bool(re.search(r'\.(png|jpg|jpeg|webp)$', str(attachment.get('filename') or ''), re.I))
        # Images are actually supplied to the vision model. A PDF URL alone is
        # not readable evidence: it needs extracted text.
        if not text and not (is_image and url in inspected_image_urls):
            issues.append(f'{kind} was not readable')
            continue
        quote = str(check.get('evidence_text') or '').strip()
        if len(quote) < 16 or (text and ' '.join(quote.lower().split()) not in ' '.join(text.lower().split())):
            issues.append(f'{kind} has no grounded document excerpt')
            continue
        name, issuer = str(check.get('patient_name') or '').strip(), str(check.get('issuer') or '').strip()
        if len(_name(name)) < 4 or len(issuer) < 3:
            issues.append(f'{kind} is missing patient or issuer details')
            continue
        try:
            document_date = date.fromisoformat(str(check.get('document_date') or ''))
            if document_date > date.today():
                raise ValueError('Future date')
        except ValueError:
            issues.append(f'{kind} has an invalid or missing document date')
            continue
        source = _source(attachment)
        if source in sources_used and sources_used[source] != kind:
            issues.append('One attachment cannot independently establish multiple required document types')
            continue
        if kind == 'cost_estimate':
            try:
                amount = Decimal(str(check.get('amount')))
                if not amount.is_finite() or amount <= 0 or str(check.get('currency') or '').upper() != 'USD':
                    raise ValueError('Invalid amount or currency')
            except (InvalidOperation, ValueError):
                issues.append('Hospital estimate needs a positive amount in the payout currency (USD)')
                continue
        if kind == 'medical_record' and (not check.get('diagnosis') or not check.get('clinician')):
            issues.append('Medical record is missing diagnosis or clinician details')
            continue
        if kind == 'government_id' and (not check.get('id_type') or not re.fullmatch(r'[A-Za-z0-9]{4}', str(check.get('id_last_four') or ''))):
            issues.append('Government identification requires a document type and last four identifier characters')
            continue
        evidence[kind] = {key: check[key] for key in (
            'document_type', 'patient_name', 'issuer', 'document_date', 'evidence_text',
            'amount', 'currency', 'diagnosis', 'clinician', 'id_type', 'id_last_four',
        ) if key in check}
        evidence[kind]['source_id'] = source
        sources_used[source] = kind
        newly_verified.add(kind)

    names = {_name(item.get('patient_name')) for item in evidence.values()}
    if len(names) > 1:
        issues.append('Patient names do not match across the documents')
    if evidence and _name(result.get('patient_name')) not in names:
        issues.append('Application patient name does not match the documents')
    missing = [kind for kind in REQUIRED if kind not in evidence]
    if not missing:
        try:
            requested = Decimal(str(result.get('requested_amount')))
            estimate = Decimal(str(evidence['cost_estimate']['amount']))
            if not requested.is_finite() or requested <= 0 or requested > estimate:
                raise ValueError('Invalid requested amount')
        except (InvalidOperation, ValueError, KeyError):
            issues.append('Requested assistance must be positive and no greater than the verified estimate')
    # A later payment-details email must not erase a previous alteration or
    # mismatch warning. Clear old issues only after a complete fresh recheck.
    if existing_issues and (newly_verified != set(REQUIRED) or issues):
        issues.extend(map(str, existing_issues))
    complete = not missing and not issues
    result['verification_evidence'] = list(evidence.values())
    result['verification_issues'] = list(dict.fromkeys(issues))
    result['is_100_percent_verified'] = complete
    result['pending_items'] = missing + (['verification_review'] if issues else [])
    result['status'] = 'approved' if complete else 'under_review'
    result['approval_source'] = DOCUMENT_CHECKS if complete else None
    result['next_action'] = ('Collect beneficiary PayPal details and submit approved assistance' if complete
                             else 'Request missing documents and resolve verification checks')
    reply = str(result.get('auto_reply_body') or '')
    if not complete and (not reply or re.search(r'\b(?:approved|paypal|100% verified)\b', reply, re.I)):
        requirements = '; '.join(REQUIRED[kind] for kind in missing)
        message = ('Please reply with ' + requirements + ' so we can continue the review.' if missing
                   else 'We need to resolve inconsistencies in the submitted documents before approving assistance.')
        result['auto_reply_body'] = (
            'Dear Applicant,\n\nThank you for your application and supporting information. '
            + message + '\n\nYour application remains under review.\n\nKind regards,\nHope Medical Assistance Team'
        )
    return result
