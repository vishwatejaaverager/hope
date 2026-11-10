"""Broad AI case review with a small execution contract, not a catalog of red flags."""
from copy import deepcopy
from typing import Any

APPROVAL_SOURCE = 'ai_red_flag_review'
REQUIRED_DOCUMENTS = {
    'government_id': 'Patient government-issued photo ID',
    'cost_estimate': 'Hospital treatment estimate or bill',
    'medical_record': 'Current medical report or treatment recommendation',
}


def document_statuses(evidence: list[dict]) -> dict:
    statuses = {}
    for kind, label in REQUIRED_DOCUMENTS.items():
        items = [item for item in evidence if item.get('document_type') == kind]
        approved = bool(items) and all(
            item.get('status') == 'approved' and item.get('readable') is True
            and str(item.get('evidence_text') or '').strip()
            and str(item.get('reason') or '').strip() and item.get('red_flags') == []
            for item in items)
        statuses[kind] = {
            'label': label, 'status': 'approved' if approved else ('needs_review' if items else 'missing'),
            'reason': '; '.join(str(item.get('reason') or 'Document verification is incomplete.') for item in items) if items else 'Document not received.',
            'source_ids': [item['source_id'] for item in items],
        }
    return statuses


def evaluate(analysis: dict[str, Any], attachments: list[dict], previous_evidence: list | None = None) -> dict[str, Any]:
    result = dict(analysis)
    flags = deepcopy(result.get('red_flags')) if isinstance(result.get('red_flags'), list) else []
    complete = result.get('review_complete') is True
    checks = result.get('document_checks')
    checks = checks if isinstance(checks, list) else []
    covered = set()
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
        from app.services.approval_policy import _source
        item = {**check, 'source_id': _source(attachments[index])}
        evidence = [old for old in evidence if old.get('source_id') != item['source_id']]
        evidence.append(item)
    if covered != set(range(len(attachments))):
        complete = False
    if not evidence:
        complete = False
    statuses = document_statuses(evidence)
    for kind, item in statuses.items():
        if item['status'] != 'approved':
            flags.append({'message': f"{item['label']}: {item['reason']}",
                          'required_action': f"Provide or resolve verification of: {item['label']}."})
    if not complete:
        flags.append({'message': 'The document review is incomplete or some evidence could not be read.',
                      'required_action': 'Provide accessible documents or clarify the incomplete review.'})
    if result.get('review_decision') != 'approve' and not flags:
        flags.append({'message': 'The reviewer did not recommend approval.',
                      'required_action': 'Clarify the remaining concerns before proceeding.'})
    approved = complete and not flags and result.get('review_decision') == 'approve'
    explanation = str(result.get('decision_explanation') or '').strip()
    if not explanation:
        approved = False
        flags.append({'message': 'No evidence-based decision explanation was provided.',
                      'required_action': 'Complete the case review.'})
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
                          'red_flags': flags, 'explanation': explanation,
                          'model': result.get('model_used'), 'document_checks': checks, 'document_statuses': statuses},
    })
    # Do not send an approval draft if the returned decision/evidence disagrees.
    reply = str(result.get('auto_reply_body') or '')
    if not approved and ('approved' in reply.lower() or not reply.strip()):
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
