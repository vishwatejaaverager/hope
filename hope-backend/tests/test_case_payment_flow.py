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
               requested_amount=Decimal('125.00'), currency='USD', status='approved', **kw)
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
    response.json.return_value = {'choices': [{'message': {'content': '{"auto_reply_body":"Hi Sara, thank you for the updated hospital bill. Please send your government ID so we can continue the review."}'}}]}
    monkeypatch.setattr(ai_service.requests, 'post', Mock(return_value=response))
    result = ai_service.analyze_incoming_email('sara@example.com', 'Updated bill', 'Here is the bill.')
    assert result['auto_reply_body'].startswith('Hi Sara, thank you')
    assert 'CASE VERIFICATION STATUS' not in result['auto_reply_body']
