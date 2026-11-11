"""Broad AI case review with a small execution contract, not a catalog of red flags."""
import hashlib
import re
from datetime import datetime, timezone
from typing import Any

APPROVAL_SOURCE = 'ai_red_flag_review'
REQUIRED_DOCUMENTS = {
    'government_id': 'Patient government-issued photo ID',
    'cost_estimate': 'Hospital treatment estimate or bill',
    'medical_record': 'Current medical report or treatment recommendation',
}


def document_verified(item):
    return (item.get('status') == 'approved' and item.get('readable') is True
            and bool(str(item.get('evidence_text') or '').strip())
            and bool(str(item.get('reason') or '').strip()) and item.get('red_flags') == [])


def document_statuses(evidence: list[dict]) -> dict:
    statuses = {}
    for kind, label in REQUIRED_DOCUMENTS.items():
        items = [item for item in evidence if item.get('document_type') == kind]
        approved = bool(items) and all(document_verified(item) for item in items)
        statuses[kind] = {
            'label': label, 'status': 'approved' if approved else ('needs_review' if items else 'missing'),
            'reason': '; '.join(str(item.get('reason') or 'Document verification is incomplete.') for item in items) if items else 'Document not received.',
            'source_ids': [item['source_id'] for item in items],
        }
    return statuses


def _flag(value):
    item = dict(value) if isinstance(value, dict) else {'message': str(value)}
    item['message'] = str(item.get('message') or 'Unresolved document concern')
    item['id'] = str(item.get('id') or 'flag-' + hashlib.sha256(item['message'].strip().lower().encode()).hexdigest()[:16])
    return item


def _supports_change(item, checks, body):
    indexes = item.get('attachment_indexes')
    indexes = indexes if isinstance(indexes, list) else []
    reviewed = {check.get('attachment_index') for check in checks if isinstance(check, dict)
                and type(check.get('attachment_index')) is int and check.get('readable') is True
                and str(check.get('evidence_text') or '').strip()}
    valid_index = any(type(index) is int and index in reviewed for index in indexes)
    excerpt = str(item.get('email_excerpt') or '').strip()
    fresh_body = re.split(r'(?m)^On .+wrote:|^-----Original Message-----', body or '')[0]
    fresh_body = '\n'.join(line for line in fresh_body.splitlines() if not line.lstrip().startswith('>'))
    return bool(str(item.get('reason') or '').strip()) and (valid_index or bool(excerpt and excerpt in fresh_body))


def evaluate(analysis: dict[str, Any], attachments: list[dict], previous_evidence: list | None = None,
             previous_report: dict | None = None, body: str | None = None) -> dict[str, Any]:
    result = dict(analysis)
    flags = [_flag(item) for item in result.get('red_flags', [])] if isinstance(result.get('red_flags'), list) else []
    complete = result.get('review_complete') is True
    checks = result.get('document_checks')
    checks = checks if isinstance(checks, list) else []
    from app.services.approval_policy import _source
    from app.services.ai_service import _extract_image_urls
    supplied_images = set(_extract_image_urls(attachments)[:4])
    covered = set()
    readable_checks = []
    evidence = [dict(item) for item in (previous_evidence or []) if isinstance(item, dict) and item.get('source_id')]
    replaced_types = {check.get('document_type') for check in checks if isinstance(check, dict)
                      and type(check.get('attachment_index')) is int
                      and 0 <= check['attachment_index'] < len(attachments)}
    evidence = [item for item in evidence if item.get('document_type') not in replaced_types]
    for check in checks:
        if not isinstance(check, dict):
            complete = False
            continue
        index = check.get('attachment_index')
        if type(index) is not int or not 0 <= index < len(attachments):
            complete = False
            continue
        if check.get('readable') is not True or not str(check.get('evidence_text') or '').strip():
            complete = False
        covered.add(index)
        item = {**check, 'source_id': _source(attachments[index])}
        if 'is_verified' in check or 'flags' in check:
            supplied = check.get('flags')
            item['red_flags'] = [flag.strip() for flag in supplied if isinstance(flag, str) and flag.strip()] if isinstance(supplied, list) else []
            item['status'] = 'approved' if check.get('is_verified') is True and supplied == [] else 'needs_review'
        if not (attachments[index].get('extracted_text') or attachments[index].get('url') in supplied_images):
            complete = False
            item.update(readable=False, status='needs_review', reason='The review service could not access readable document content.',
                        red_flags=['Readable content was unavailable to the model.'])
        if item.get('readable') is True:
            readable_checks.append(item)
        evidence = [old for old in evidence if old.get('source_id') != item['source_id']]
        evidence.append(item)
    prior = previous_report if isinstance(previous_report, dict) else {}
    unresolved = {_flag(item)['id']: _flag(item) for item in prior.get('red_flags', [])
                  if not isinstance(item, dict) or item.get('origin') != 'computed'}
    resolved = []
    resolutions = result.get('resolved_red_flags')
    for resolution in resolutions if isinstance(resolutions, list) else []:
        if not isinstance(resolution, dict):
            continue
        flag_id = resolution.get('flag_id')
        if flag_id in unresolved and _supports_change(resolution, readable_checks, body):
            resolved.append({**unresolved.pop(flag_id), 'resolution': resolution})
    merged_flags = {flag['id']: {**flag, 'origin': 'ai'} for flag in flags}
    # A reused ID cannot silently rewrite an unresolved concern away.
    for flag_id, old in unresolved.items():
        merged_flags[flag_id] = {**merged_flags.get(flag_id, {}), **old}
    flags = list(merged_flags.values())
    updates = result.get('previous_document_updates')
    for update in updates if isinstance(updates, list) else []:
        if not isinstance(update, dict):
            continue
        for item in evidence:
            if item.get('source_id') != update.get('source_id'):
                continue
            if update.get('status') == 'needs_review' and str(update.get('reason') or '').strip():
                item.update(status='needs_review', reason=update['reason'], red_flags=update.get('red_flags') or [update['reason']])
            elif update.get('status') == 'approved' and update.get('red_flags') == [] and _supports_change(update, readable_checks, body):
                item.update(status='approved', reason=update['reason'], red_flags=[])
    previous_sources = {old.get('source_id') for old in (previous_evidence or []) if isinstance(old, dict)}
    # A contradiction can reopen an older document without re-uploading it.
    for flag in flags:
        sources = flag.get('source_ids') if isinstance(flag.get('source_ids'), list) else []
        indexes = flag.get('attachment_indexes') if isinstance(flag.get('attachment_indexes'), list) else []
        for item in evidence:
            if item.get('source_id') in sources or (item.get('source_id') not in previous_sources and item.get('attachment_index') in indexes):
                item.update(status='needs_review', reason=flag['message'], red_flags=[flag['message']])
    if covered != set(range(len(attachments))):
        complete = False
    if not evidence:
        complete = False
    current_sources = {_source(attachment) for attachment in attachments}
    current = [item for item in evidence if item['source_id'] in current_sources]
    for item in evidence:
        item['is_verified'] = document_verified(item)
        item['flags'] = [] if item['is_verified'] else [
            str(flag.get('message') or 'Review incomplete.') if isinstance(flag, dict) else str(flag)
            for flag in (item.get('red_flags') or [item.get('reason') or 'Review incomplete.'])
        ]
    for item in evidence:
        for message in item['flags']:
            flags.append({'origin': 'computed', 'message': message,
                          'required_action': 'Please clarify the issue or send a corrected document.'})
    statuses = document_statuses(evidence)
    for kind, item in statuses.items():
        if item['status'] != 'approved':
            flags.append({'origin': 'computed', 'message': f"{item['label']}: {item['reason']}",
                          'required_action': f"Provide or resolve verification of: {item['label']}."})
    if not complete:
        flags.append({'origin': 'computed', 'message': 'The document review is incomplete or some evidence could not be read.',
                      'required_action': 'Provide accessible documents or clarify the incomplete review.'})
    if result.get('review_decision') != 'approve' and not flags:
        flags.append({'origin': 'computed', 'message': 'The reviewer did not recommend approval.',
                      'required_action': 'Clarify the remaining concerns before proceeding.'})
    approved = complete and not flags and result.get('review_decision') == 'approve'
    explanation = str(result.get('decision_explanation') or '').strip()
    if not explanation:
        approved = False
        flags.append({'origin': 'computed', 'message': 'No evidence-based decision explanation was provided.',
                      'required_action': 'Complete the case review.'})
    flags = [_flag(flag) for flag in flags]
    issues = [str(flag.get('message') or 'Unresolved review concern') if isinstance(flag, dict) else str(flag) for flag in flags]
    result.update({
        'status': 'approved' if approved else 'under_review',
        'approval_source': APPROVAL_SOURCE if approved else None,
        'is_100_percent_verified': approved,
        'verification_evidence': evidence,
        'verification_issues': issues,
        'pending_items': [str(flag.get('required_action') or flag.get('message')) if isinstance(flag, dict) else str(flag) for flag in flags],
        'next_action': 'Arrange approved assistance through the payment workflow' if approved else 'Resolve the concerns identified in the case review',
        'review_report': {'review_complete': complete, 'decision': 'approve' if approved else 'request_information',
                          'red_flags': flags, 'resolved_red_flags': resolved,
                          'reviewed_at': datetime.now(timezone.utc).isoformat(), 'explanation': explanation,
                          'model': result.get('model_used'),
                          'document_checks': current,
                          'document_statuses': statuses},
    })
    # Do not send an approval draft if the returned decision/evidence disagrees.
    reply = str(result.get('auto_reply_body') or '')
    verdict_changed = any(
        isinstance(check, dict) and check.get('is_verified') is True
        and not any(item.get('attachment_index') == check.get('attachment_index')
                    and item['is_verified'] for item in current)
        for check in checks
    )
    if verdict_changed:
        # A draft based on a superseded verdict could falsely confirm a document.
        findings = list(dict.fromkeys(message for item in current for message in item['flags']))
        result['auto_reply_body'] = (
            'Dear Applicant,\n\nThank you for sending your documents. We need clarification before we can complete the review.\n\n'
            + '\n'.join(f'- {message}' for message in findings)
            + '\n\nPlease reply with clarification or a corrected document.\n\nKind regards,\nHope Medical Assistance Team'
        )
    elif not approved and ('approved' in reply.lower() or not reply.strip()):
        actions = '\n'.join('- ' + str(flag.get('required_action') or flag.get('message')) if isinstance(flag, dict) else '- ' + str(flag) for flag in flags)
        result['auto_reply_body'] = ('Dear Applicant,\n\nThank you for your submission. We need the following information before completing your application:\n\n'
                                     + actions + '\n\nPlease reply in this thread.\n\nKind regards,\nHope Medical Assistance Team')
    return result


def authorizes_payment(report: Any) -> bool:
    return (isinstance(report, dict) and report.get('review_complete') is True
            and report.get('decision') == 'approve' and report.get('red_flags') == []
            and bool(str(report.get('explanation') or '').strip())
            and all(isinstance(report.get('document_statuses', {}).get(kind), dict)
                    and report['document_statuses'][kind].get('status') == 'approved'
                    for kind in REQUIRED_DOCUMENTS))
