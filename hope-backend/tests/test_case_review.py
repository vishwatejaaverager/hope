from copy import deepcopy
from decimal import Decimal
from app.services import case_review, approval_policy, case_workflow, ai_service
from app.models import Case, Payout, OutgoingEmail
from tests.test_case_payment_flow import client, db_session, setup_database, isolate, TEST_SECRET
from unittest.mock import Mock
from sqlalchemy import select


def report():
    return {'patient_name': 'Test Patient', 'requested_amount': '100.00', 'document_checks': [
        {'attachment_index': index, 'document_type': kind, 'readable': True, 'status': 'approved', 'reason': 'Consistent current evidence.', 'red_flags': [],
         'evidence_text': 'Evidence read from the complete application bundle.'}
        for index, kind in enumerate(case_review.REQUIRED_DOCUMENTS)],
        'review_complete': True, 'red_flags': [], 'review_decision': 'approve',
        'decision_explanation': 'The application is supported by consistent, current evidence and the assistance amount is established.',
        'auto_reply_body': 'Dear Applicant, your application is approved. Thank you for providing the supporting documents.'}


def attachments():
    return [{'filename': kind + '.png', 'url': 'https://example.com/' + kind + '.png'} for kind in case_review.REQUIRED_DOCUMENTS]


def test_no_flags_complete_review_approves():
    result = case_review.evaluate(report(), attachments())
    assert result['status'] == 'approved'
    assert case_review.authorizes_payment(result['review_report'])


def test_any_red_flag_blocks_approval():
    original = report()
    original['red_flags'] = [{'message': 'The estimate has expired.', 'supporting_evidence': 'Valid until 15 February 2026',
                              'required_action': 'Provide a current estimate.'}]
    result = case_review.evaluate(original, attachments())
    assert result['status'] == 'under_review'
    assert not case_review.authorizes_payment(result['review_report'])
    assert 'Provide a current estimate.' in result['auto_reply_body']
    assert 'is approved' not in result['auto_reply_body']


def test_empty_flags_do_not_approve_incomplete_review():
    original = report()
    original['review_complete'] = False
    result = case_review.evaluate(original, attachments())
    assert result['status'] == 'under_review'
    assert not case_review.authorizes_payment(result['review_report'])


def test_unreviewed_attachment_blocks_approval():
    result = case_review.evaluate(report(), [{'filename': 'one.png'}, {'filename': 'two.png'}])
    assert result['status'] == 'under_review'


def test_case_review_is_saved_and_drafted_email_sent(client, db_session, monkeypatch):
    result = report()
    result['review_decision'] = 'request_information'
    result['red_flags'] = [{'message': 'Conflicting dates in the documents.', 'required_action': 'Please clarify the dates.'}]
    result['auto_reply_body'] = 'Dear Applicant, please clarify the conflicting dates shown in your documents.'
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value=result))
    response = client.post('/api/v1/emails/incoming', headers={'X-Webhook-Secret': TEST_SECRET}, json={
        'message_id': 'broad-review', 'sender': 'patient@example.com', 'recipient': 'support@hope.org',
        'body_plain': 'Please review.', 'attachment_metadata': [{'filename': 'application.png', 'url': 'https://example.com/application.png'}]})
    assert response.status_code == 201
    assert response.json()['auto_reply_body'] == result['auto_reply_body']
    case = db_session.execute(select(Case)).scalar_one()
    assert case.review_report['red_flags'][0]['message'] == 'Conflicting dates in the documents.'
    assert case.status == 'under_review'
    assert db_session.execute(select(OutgoingEmail)).scalar_one().body_plain == result['auto_reply_body']
    assert not db_session.execute(select(Payout)).scalars().all()


def test_individual_document_fields_are_independent():
    original = report()
    original['document_checks'][1].update(status='needs_review', reason='Estimate expired.', red_flags=['Expired'])
    result = case_review.evaluate(original, attachments())
    statuses = result['review_report']['document_statuses']
    assert statuses['government_id']['status'] == 'approved'
    assert statuses['cost_estimate']['status'] == 'needs_review'
    assert statuses['medical_record']['status'] == 'approved'
    assert result['status'] == 'under_review'


def test_missing_required_document_cannot_be_approved():
    original = report()
    original['document_checks'] = original['document_checks'][:1]
    result = case_review.evaluate(original, attachments()[:1])
    assert result['review_report']['document_statuses']['cost_estimate']['status'] == 'missing'
    assert result['status'] == 'under_review'


def test_followup_preserves_previously_approved_document():
    original = report()
    original['document_checks'] = original['document_checks'][:1]
    first = case_review.evaluate(original, attachments()[:1])
    followup = report()
    followup['document_checks'] = followup['document_checks'][1:]
    for index, check in enumerate(followup['document_checks']):
        check['attachment_index'] = index
    final = case_review.evaluate(followup, attachments()[1:], first['verification_evidence'])
    assert final['status'] == 'approved'


def test_approved_document_fields_are_persisted(client, db_session, monkeypatch):
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value=report()))
    response = client.post('/api/v1/emails/incoming', headers={'X-Webhook-Secret': TEST_SECRET}, json={
        'message_id': 'three-approved-documents', 'sender': 'patient@example.com',
        'recipient': 'support@hope.org', 'body_plain': 'Please review my application.',
        'attachment_metadata': [{**item, 'url': 'https://example.com/' + item['filename']} for item in attachments()]})
    assert response.status_code == 201
    case = db_session.execute(select(Case)).scalar_one()
    assert case.status == 'approved'
    assert all(item['status'] == 'approved' for item in case.review_report['document_statuses'].values())
    assert 'PayPal' in response.json()['auto_reply_body']
    assert 'Thank you for providing' in response.json()['auto_reply_body']
    assert not db_session.execute(select(Payout)).scalars().all()
