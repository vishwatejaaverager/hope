from decimal import Decimal
from unittest.mock import Mock
import pytest
from sqlalchemy import select
from tests.test_case_management import client, db_session, setup_database, TEST_SECRET
from app.models import Case, Payout, OutgoingEmail
from app.services import ai_service, case_workflow, paypal_service, smtp_service

@pytest.fixture(autouse=True)
def isolate(monkeypatch):
    monkeypatch.setenv('DISABLE_OPENROUTER_IN_TESTS', '1')
    monkeypatch.setattr('app.api.routes.email.requests.post', Mock())
    monkeypatch.setattr(smtp_service, 'smtp_configured', lambda: False)
    monkeypatch.setattr(paypal_service, 'create_payout', Mock(side_effect=AssertionError('Unexpected payout')))
    monkeypatch.setattr(paypal_service, 'get_payout', Mock(side_effect=AssertionError('Unexpected lookup')))

def make_case(db, **kw):
    row = Case(case_number='CASE-PAYMENT-01', patient_name='Sara', patient_email='sara@example.com',
               requested_amount=Decimal('125.00'), currency='USD', status='approved', approval_source='reviewer', **kw)
    db.add(row); db.commit()
    return row

def incoming(client, case, body, mid='message-1'):
    return client.post('/api/v1/emails/incoming', headers={'X-Webhook-Secret': TEST_SECRET}, json={
        'message_id': mid, 'sender': case.patient_email, 'recipient': 'support@hope.org',
        'subject': f'Re: {case.case_number}', 'body_plain': body})

def mock_paypal(monkeypatch, status='SUCCESS'):
    data = {'batch_header': {'payout_batch_id': 'PAYPAL123', 'batch_status': 'SUCCESS'},
            'items': [{'transaction_status': status, 'payout_item_id': 'ITEM123'}]}
    create = Mock(return_value=data)
    monkeypatch.setattr(paypal_service, 'create_payout', create)
    monkeypatch.setattr(paypal_service, 'get_payout', Mock(return_value=data))
    return create

def test_approval_requests_paypal_without_using_contact(client, db_session):
    case = make_case(db_session)
    res = incoming(client, case, 'Any update?')
    assert res.status_code == 201
    assert 'PayPal account' in res.json()['auto_reply_body']
    assert 'CASE VERIFICATION STATUS' not in res.json()['auto_reply_body']
    assert case.status == 'approved'
    assert case.paypal_email is None
    assert not db_session.execute(select(Payout)).scalars().all()

def test_paypal_reply_pays_once(client, db_session, monkeypatch):
    case = make_case(db_session)
    create = mock_paypal(monkeypatch)
    incoming(client, case, 'Any update?', 'request-email')
    res = incoming(client, case, 'My PayPal email is beneficiary@example.com', 'paypal-email')
    assert res.status_code == 201
    assert 'confirmed your payment of $125.00' in res.json()['auto_reply_body']
    assert case.status == 'disbursed'
    assert create.call_args.args[:2] == ('beneficiary@example.com', '125.00')
    incoming(client, case, 'Thanks', 'thanks')
    incoming(client, case, 'My PayPal email is beneficiary@example.com', 'paypal-email')
    assert create.call_count == 1
    assert len(db_session.execute(select(Payout)).scalars().all()) == 1

def test_existing_paypal_pays_on_approval(client, db_session, monkeypatch):
    case = make_case(db_session, paypal_email='payee@example.com')
    case.status = 'under_review'; db_session.commit()
    create = mock_paypal(monkeypatch, 'PENDING')
    res = client.patch(f'/api/v1/cases/{case.id}', headers={'X-Webhook-Secret': TEST_SECRET}, json={'status': 'approved'})
    assert res.status_code == 200
    assert res.json()['status'] == 'payout_processing'
    assert create.call_count == 1
    assert 'completion is not yet confirmed' in db_session.execute(select(OutgoingEmail)).scalar_one().body_plain

def test_timeout_reuses_frozen_details(db_session, monkeypatch):
    case = make_case(db_session, paypal_email='payee@example.com')
    create = Mock(side_effect=paypal_service.PayPalError('Timeout'))
    monkeypatch.setattr(paypal_service, 'create_payout', create)
    case_workflow.process_approved_case(db_session, case)
    first = create.call_args
    case.requested_amount = Decimal('999.00'); case.paypal_email = 'different@example.com'
    case_workflow.process_approved_case(db_session, case)
    assert create.call_args == first
    assert case.status == 'payout_processing'
    assert len(db_session.execute(select(Payout)).scalars().all()) == 1

def test_missing_amount_never_uses_estimate(db_session):
    case = make_case(db_session, paypal_email='payee@example.com')
    case.requested_amount = None; case.estimated_cost = Decimal('20000.00')
    assert 'confirm the approved assistance amount' in case_workflow.process_approved_case(db_session, case)
    assert not db_session.execute(select(Payout)).scalars().all()

def test_fallback_does_not_verify_attachment_claim():
    result = ai_service._heuristic_fallback_analysis('sara@example.com', 'Application',
        'Attached government ID, hospital bill and admission report.', [{'filename': 'id_bill_report.pdf'}])
    assert result['status'] != 'approved'
    assert result['is_100_percent_verified'] is False
    assert 'CASE VERIFICATION STATUS' not in result['auto_reply_body']

def test_explicit_paypal_details_only():
    assert case_workflow.extract_paypal_email('Contact my doctor at doctor@example.com') is None
    assert case_workflow.extract_paypal_email('PayPal is not working. Contact doctor@example.com') is None
    assert case_workflow.extract_paypal_email('This is not my PayPal: wrong@example.com') is None
    assert case_workflow.extract_paypal_email('payee@example.com', awaiting_email=True) == 'payee@example.com'
    assert case_workflow.extract_paypal_email('Thanks\n> PayPal: old@example.com') is None

def test_unapproved_case_cannot_disburse(client, db_session):
    case = make_case(db_session, paypal_email='payee@example.com')
    case.status = 'under_review'; db_session.commit()
    res = client.post(f'/api/v1/cases/{case.id}/disburse', headers={'X-Webhook-Secret': TEST_SECRET}, json={})
    assert res.status_code == 409

def test_bare_address_after_request(client, db_session, monkeypatch):
    case = make_case(db_session)
    create = mock_paypal(monkeypatch)
    incoming(client, case, 'Any update?', 'first')
    res = incoming(client, case, 'payee@example.com', 'second')
    assert res.status_code == 201
    assert create.call_args.args[0] == 'payee@example.com'


def test_failed_payout_does_not_mark_case_paid(db_session, monkeypatch):
    case = make_case(db_session, paypal_email='payee@example.com')
    create = mock_paypal(monkeypatch, 'FAILED')
    reply = case_workflow.process_approved_case(db_session, case)
    assert 'has not completed' in reply
    assert case.status == 'payout_processing'
    case_workflow.process_approved_case(db_session, case)
    assert create.call_count == 1


def test_ai_reply_does_not_receive_status_template(monkeypatch):
    monkeypatch.delenv('DISABLE_OPENROUTER_IN_TESTS')
    monkeypatch.setattr(ai_service, 'get_openrouter_api_key', lambda: 'test-key')
    response = Mock(ok=True)
    response.json.return_value = {'choices': [{'message': {'content': '{"document_checks":[],"verification_issues":[],"auto_reply_body":"Hi Sara, thank you for the updated hospital bill. Please send your government ID so we can continue the review."}'}}]}
    monkeypatch.setattr(ai_service.requests, 'post', Mock(return_value=response))
    result = ai_service.analyze_incoming_email('sara@example.com', 'Updated bill', 'Here is the bill.')
    assert result['auto_reply_body'].startswith('Hi Sara, thank you')
    assert 'CASE VERIFICATION STATUS' not in result['auto_reply_body']


def test_zapier_five_field_application_payload(client, db_session):
    payload = {
        'message_id': '<ramesh-application-test@example.com>',
        'sender': 'ramesh-test@example.com',
        'recipient': 'support@hope.org',
        'subject': 'Medical Assistance Request — Ramesh Kumar — Heart Bypass Surgery',
        'body_plain': 'Dear Hope Medical Assistance Team, I am requesting financial assistance of USD 125 toward treatment at Apollo Hospitals, Hyderabad. I currently have only the consultation and prescription document. Please advise which additional documents are required.',
    }
    response = client.post('/api/v1/emails/incoming', json=payload,
                           headers={'X-Webhook-Secret': TEST_SECRET})
    assert response.status_code == 201
    assert response.json()['status'] == 'received'
    assert response.json()['outgoing_email_id']
    assert response.json()['auto_reply_recipient'] == payload['sender']
    assert response.json()['auto_reply_body']
    assert db_session.execute(select(OutgoingEmail)).scalar_one().status == 'pending'


def test_single_prescription_cannot_be_auto_approved(client, db_session, monkeypatch):
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value={
        'patient_name': 'Ramesh Kumar', 'patient_email': 'applicant@example.com',
        'requested_amount': 125, 'status': 'approved',
        'is_100_percent_verified': True, 'pending_items': [],
        'auto_reply_body': 'Your case is approved. Please send your PayPal email.',
    }))
    response = client.post('/api/v1/emails/incoming', headers={'X-Webhook-Secret': TEST_SECRET}, json={
        'message_id': 'single-prescription', 'sender': 'applicant@example.com',
        'recipient': 'support@hope.org', 'subject': 'Medical assistance request',
        'body_plain': 'I have only the consultation and prescription document. Do I need a cost estimate and identification?',
        'attachment_metadata': [{'filename': '1.png', 'content_type': 'image/png', 'url': 'https://example.com/1.png'}],
    })
    assert response.status_code == 201
    case = db_session.execute(select(Case)).scalar_one()
    assert case.status != 'approved'
    reply = response.json()['auto_reply_body'].lower()
    assert 'case is approved' not in reply
    assert 'estimate' in reply
    assert 'identification' in reply or 'government id' in reply
    assert not db_session.execute(select(Payout)).scalars().all()


def test_old_unattributed_approval_cannot_trigger_payment(client, db_session):
    case = make_case(db_session, paypal_email='payee@example.com')
    case.approval_source = None
    db_session.commit()
    response = incoming(client, case, 'My PayPal email is payee@example.com', 'legacy-approval')
    assert response.status_code == 201
    assert case.status == 'under_review'
    assert 'case is approved' not in response.json()['auto_reply_body'].lower()
    assert not db_session.execute(select(Payout)).scalars().all()


def document_fixture():
    definitions = [
        ('medical_record', 'Medical consultation for Ramesh Kumar: coronary artery disease.', {'diagnosis': 'Coronary artery disease', 'clinician': 'Dr Rao'}),
        ('cost_estimate', 'Hospital estimate for Ramesh Kumar: treatment costs USD 500.', {'amount': '500.00', 'currency': 'USD'}),
        ('government_id', 'Government identification issued to Ramesh Kumar, reference ending 1234.', {'id_type': 'national_id', 'id_last_four': '1234'}),
    ]
    attachments, checks = [], []
    for index, (kind, quote, details) in enumerate(definitions):
        attachments.append({'filename': f'{kind}.txt', 'content_type': 'text/plain', 'extracted_text': quote})
        checks.append({'document_type': kind, 'attachment_index': index, 'verdict': 'verified',
                       'patient_name': 'Ramesh Kumar', 'issuer': 'Test issuing authority',
                       'document_date': '2026-11-01', 'evidence_text': quote, **details})
    return attachments, checks


def test_complete_document_checks_approve_and_pay_automatically(client, db_session, monkeypatch):
    attachments, checks = document_fixture()
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value={
        'patient_name': 'Ramesh Kumar', 'requested_amount': '125.00',
        'status': 'under_review', 'document_checks': checks, 'verification_issues': [],
        'auto_reply_body': 'Thank you for the supporting documents.',
    }))
    create = mock_paypal(monkeypatch)
    response = client.post('/api/v1/emails/incoming', headers={'X-Webhook-Secret': TEST_SECRET}, json={
        'message_id': 'complete-documents', 'sender': 'ramesh@example.com', 'recipient': 'support@hope.org',
        'subject': 'Medical assistance', 'body_plain': 'My PayPal email is payee@example.com',
        'attachment_metadata': attachments,
    })
    assert response.status_code == 201
    case = db_session.execute(select(Case)).scalar_one()
    assert case.status == 'disbursed'
    assert case.approval_source == 'document_checks'
    assert len(case.verification_evidence) == 3
    assert create.call_args.args[:2] == ('payee@example.com', '125.00')


def test_mismatched_identity_blocks_automatic_approval():
    from app.services.approval_policy import constrain_email_analysis
    attachments, checks = document_fixture()
    checks[2]['patient_name'] = 'Different Patient'
    result = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125,
                                       'document_checks': checks}, 'test@example.com', None, '', attachments)
    assert result['status'] == 'under_review'
    assert 'Patient names do not match across the documents' in result['verification_issues']


def test_one_attachment_cannot_claim_all_document_types():
    from app.services.approval_policy import constrain_email_analysis
    attachments, checks = document_fixture()
    for check in checks:
        check['attachment_index'] = 0
        check['evidence_text'] = attachments[0]['extracted_text']
    result = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125,
                                       'document_checks': checks}, 'test@example.com', None, '', attachments[:1])
    assert result['status'] == 'under_review'
    assert 'cost_estimate' in result['pending_items']
    assert 'government_id' in result['pending_items']


def test_document_checks_accumulate_across_emails():
    from app.services.approval_policy import constrain_email_analysis
    attachments, checks = document_fixture()
    first = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125,
                                      'document_checks': checks[:1]}, 'test@example.com', None, '', attachments[:1])
    assert first['status'] == 'under_review'
    for check in checks[1:]:
        check['attachment_index'] -= 1
    second = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125,
                                       'document_checks': checks[1:]}, 'test@example.com', None, '', attachments[1:],
                                       existing_evidence=first['verification_evidence'])
    assert second['status'] == 'approved'
    assert second['pending_items'] == []


def test_fabricated_excerpt_or_unresolved_issue_blocks_approval():
    from app.services.approval_policy import constrain_email_analysis
    attachments, checks = document_fixture()
    checks[1]['evidence_text'] = 'This text does not exist in the attachment.'
    result = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125,
                                       'document_checks': checks}, 'test@example.com', None, '', attachments)
    assert result['status'] == 'under_review'
    attachments, checks = document_fixture()
    result = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125,
                                       'document_checks': checks, 'verification_issues': ['Possible alteration']},
                                      'test@example.com', None, '', attachments)
    assert result['status'] == 'under_review'


def test_usd_amount_is_not_truncated_in_fallback():
    result = ai_service._heuristic_fallback_analysis('test@example.com', None, 'I request USD 125 for treatment.', [])
    assert result['requested_amount'] == 125


def test_verification_warning_survives_later_payment_email():
    from app.services.approval_policy import constrain_email_analysis
    attachments, checks = document_fixture()
    first = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125,
                                      'document_checks': checks, 'verification_issues': ['Possible alteration']},
                                     'test@example.com', None, '', attachments)
    next_result = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125},
        'test@example.com', None, 'My PayPal email is payee@example.com', [],
        existing_evidence=first['verification_evidence'], existing_issues=first['verification_issues'])
    assert next_result['status'] == 'under_review'
    assert 'Possible alteration' in next_result['verification_issues']


def test_pdf_url_without_readable_text_cannot_establish_verification():
    from app.services.approval_policy import constrain_email_analysis
    attachments, checks = document_fixture()
    for attachment in attachments:
        attachment.pop('extracted_text')
        attachment['content_type'] = 'application/pdf'
        attachment['url'] = 'https://example.com/document.pdf'
    result = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125,
                                       'document_checks': checks}, 'test@example.com', None, '', attachments)
    assert result['status'] == 'under_review'
    assert result['verification_evidence'] == []


def test_readable_prescription_only_requests_estimate_and_id():
    from app.services.approval_policy import constrain_email_analysis
    attachments, checks = document_fixture()
    attachments = [{'filename': '1.png', 'content_type': 'image/png', 'url': 'https://example.com/prescription.png'}]
    result = constrain_email_analysis({'patient_name': 'Ramesh Kumar', 'requested_amount': 125,
                                       'document_checks': checks[:1], 'status': 'approved',
                                       'auto_reply_body': 'Your case is approved.'},
                                      'test@example.com', None, '', attachments)
    assert result['status'] == 'under_review'
    assert set(result['pending_items']) == {'cost_estimate', 'government_id'}
    assert 'estimate' in result['auto_reply_body']
    assert 'identification' in result['auto_reply_body']


@pytest.mark.parametrize('failure', ['http_error', 'timeout', 'invalid_json', 'incomplete_json'])
def test_all_model_failures_return_failure_notice(monkeypatch, failure):
    monkeypatch.delenv('DISABLE_OPENROUTER_IN_TESTS')
    monkeypatch.delenv('OPENROUTER_MODEL', raising=False)
    monkeypatch.setattr(ai_service, 'get_openrouter_api_key', lambda: 'test-key')
    response = Mock(ok=False, status_code=503, text='Unavailable')
    if failure in {'invalid_json', 'incomplete_json'}:
        response.ok = True
        response.json.return_value = {'choices': [{'message': {'content': 'not JSON' if failure == 'invalid_json' else '{}'}}]}
    post = Mock(return_value=response)
    if failure == 'timeout':
        post.side_effect = ai_service.requests.Timeout('Provider timed out')
    monkeypatch.setattr(ai_service.requests, 'post', post)
    result = ai_service.analyze_incoming_email('applicant@example.com', 'Application', 'Please review my documents.')
    assert post.call_count == len(ai_service.FALLBACK_MODELS)
    assert result['analysis_status'] == 'failed'
    assert result['failure_reason'] == 'all_models_failed'
    assert 'could not complete the document review' in result['auto_reply_body']
    assert result['is_100_percent_verified'] is False


def test_missing_key_returns_failure_notice_without_provider_call(monkeypatch):
    monkeypatch.delenv('DISABLE_OPENROUTER_IN_TESTS')
    monkeypatch.setattr(ai_service, 'get_openrouter_api_key', lambda: None)
    post = Mock()
    monkeypatch.setattr(ai_service.requests, 'post', post)
    result = ai_service.analyze_incoming_email('applicant@example.com', 'Application', 'Review please.')
    post.assert_not_called()
    assert result['failure_reason'] == 'analysis_not_configured'


@pytest.mark.parametrize('already_approved', [False, True])
def test_failed_analysis_queues_notice_without_payment_or_erasing_evidence(client, db_session, monkeypatch, already_approved):
    case = make_case(db_session, paypal_email='payee@example.com')
    case.status = 'approved' if already_approved else 'under_review'
    case.overall_summary = 'Existing case summary'
    case.verification_evidence = [{'document_type': 'medical_record', 'patient_name': 'Sara'}]
    case.verification_issues = ['Identity needs clarification']
    db_session.commit()
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value=ai_service._analysis_failure(
        case.patient_email, f'Re: {case.case_number}', 'all_models_failed')))
    response = incoming(client, case, 'My PayPal email is payee@example.com', 'failed-review')
    assert response.status_code == 201
    assert 'could not complete the document review' in response.json()['auto_reply_body']
    assert case.status == ('approved' if already_approved else 'under_review')
    assert case.overall_summary == 'Existing case summary'
    assert case.verification_evidence == [{'document_type': 'medical_record', 'patient_name': 'Sara'}]
    assert case.verification_issues == ['Identity needs clarification']
    assert 'document_analysis_retry' in case.pending_items
    outgoing = db_session.execute(select(OutgoingEmail)).scalar_one()
    assert outgoing.recipient_email == case.patient_email
    assert outgoing.reply_to_message_id == 'failed-review'
    assert outgoing.raw_payload['analysis_status'] == 'failed'
    assert outgoing.raw_payload['auto_generated_by_ai'] is False
    assert not db_session.execute(select(Payout)).scalars().all()


def test_successful_fallback_model_does_not_send_failure_notice(monkeypatch):
    monkeypatch.delenv('DISABLE_OPENROUTER_IN_TESTS')
    monkeypatch.delenv('OPENROUTER_MODEL', raising=False)
    monkeypatch.setattr(ai_service, 'get_openrouter_api_key', lambda: 'test-key')
    failed = Mock(ok=False, status_code=503, text='Unavailable')
    success = Mock(ok=True)
    success.json.return_value = {'choices': [{'message': {'content': '{"document_checks":[],"verification_issues":[],"auto_reply_body":"Thank you for submitting your documents."}'}}]}
    post = Mock(side_effect=[failed, success])
    monkeypatch.setattr(ai_service.requests, 'post', post)
    result = ai_service.analyze_incoming_email('test@example.com', 'Application', 'Review please.')
    assert post.call_count == 2
    assert result['analysis_status'] == 'completed'
    assert 'failure_reason' not in result
    assert result['auto_reply_body'] == 'Thank you for submitting your documents.'
