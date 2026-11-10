from email.message import EmailMessage
from unittest.mock import Mock

from sqlalchemy import func, select
from tests.test_email_webhook import client, db_session, setup_database, TestingSessionLocal, TEST_SECRET
from app.models import EmailAttachment, IncomingEmail, OutgoingEmail
from app.services import ai_service, imap_service

HEADERS = {'X-Webhook-Secret': TEST_SECRET}


def seed(client, message_id):
    return client.post('/api/v1/emails/incoming', headers=HEADERS, json={
        'message_id': message_id, 'sender': 'patient@example.com', 'recipient': 'support@hope.org',
        'subject': 'Medical assistance', 'body_plain': 'Document attached.',
        'ai_summary': 'Explicitly seeded without analysis',
    })


def test_dashboard_recovers_files_saved_without_email_metadata(client, db_session):
    assert seed(client, 'saved-file').status_code == 201
    file = EmailAttachment(message_id='saved-file', filename='prescription.png', content_type='image/png',
                           size=13, data=b'image-fixture')
    db_session.add(file); db_session.commit()
    response = client.get('/api/v1/emails/incoming', headers=HEADERS)
    assert response.status_code == 200
    row = response.json()[0]
    assert row['attachment_count'] == 1
    assert row['attachment_metadata'][0]['filename'] == 'prescription.png'
    download = client.get(f'/api/v1/emails/attachments/{file.id}')
    assert download.status_code == 200
    assert download.content == b'image-fixture'


def test_richer_duplicate_adds_documents_without_repeating_analysis(client, db_session, monkeypatch):
    assert seed(client, 'richer-duplicate').status_code == 201
    analysis = Mock(side_effect=AssertionError('Duplicate delivery must not rerun analysis'))
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', analysis)
    response = client.post('/api/v1/emails/incoming', headers=HEADERS, json={
        'message_id': 'richer-duplicate', 'sender': 'patient@example.com', 'recipient': 'support@hope.org',
        'attachment_metadata': [{'filename': 'bill.png', 'url': 'https://example.com/bill.png'}],
    })
    assert response.status_code == 200
    assert response.json()['duplicate'] is True
    stored = db_session.execute(select(IncomingEmail)).scalar_one()
    assert stored.attachment_count == 1
    assert stored.attachment_metadata[0]['filename'] == 'bill.png'
    analysis.assert_not_called()
    assert db_session.execute(select(func.count()).select_from(OutgoingEmail)).scalar_one() == 0


def test_imap_does_not_drop_files_when_zapier_stored_text_first(client, db_session, monkeypatch):
    message_id = '<mail-race@example.com>'
    assert seed(client, message_id).status_code == 201
    message = EmailMessage()
    message['Message-ID'] = message_id
    message['From'] = 'patient@example.com'
    message['To'] = 'support@hope.org'
    message['Subject'] = 'Document submission'
    message.set_content('Document attached.')
    message.add_attachment(b'image-fixture', maintype='image', subtype='png', filename='prescription.png')
    monkeypatch.setattr(imap_service, 'SessionLocal', TestingSessionLocal)
    post = Mock(side_effect=AssertionError('Existing email must be enriched without a second webhook'))
    monkeypatch.setattr(imap_service.requests, 'post', post)
    assert imap_service._process_message(message.as_bytes()) is True
    assert imap_service._process_message(message.as_bytes()) is True
    post.assert_not_called()
    db_session.expire_all()
    stored = db_session.execute(select(IncomingEmail)).scalar_one()
    assert stored.attachment_count == 1
    assert '/api/v1/emails/attachments/' in stored.attachment_metadata[0]['url']
    assert db_session.execute(select(func.count()).select_from(EmailAttachment)).scalar_one() == 1


def test_text_only_zapier_waits_for_authoritative_mailbox_delivery(client, db_session, monkeypatch):
    monkeypatch.setattr(imap_service, 'imap_configured', lambda: True)
    analysis = Mock(side_effect=AssertionError('Do not review an incomplete Zapier event'))
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', analysis)
    response = client.post('/api/v1/emails/incoming', headers=HEADERS, json={
        'message_id': 'wait-for-files', 'sender': 'patient@example.com', 'recipient': 'support@hope.org',
        'subject': 'Application', 'body_plain': 'Prescription attached.',
    })
    assert response.status_code == 202
    assert response.json()['status'] == 'awaiting_mailbox'
    analysis.assert_not_called()
    queued = db_session.execute(select(IncomingEmail)).scalar_one()
    assert queued.raw_payload['intake_status'] == 'awaiting_mailbox'
    assert db_session.execute(select(func.count()).select_from(OutgoingEmail)).scalar_one() == 0


def test_complete_mailbox_delivery_is_not_deferred(db_session, monkeypatch):
    from fastapi.testclient import TestClient
    from app.main import app
    from app.db import get_db
    monkeypatch.setattr(imap_service, 'imap_configured', lambda: True)
    monkeypatch.setattr(imap_service, 'start_poller', Mock())
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app, client=('127.0.0.1', 12345)) as local:
            response = local.post('/api/v1/emails/incoming', headers=HEADERS, json={
                'message_id': 'complete-mailbox', 'sender': 'patient@example.com', 'recipient': 'support@hope.org',
                'body_plain': 'No attachments on this actual message.', 'ai_summary': 'No review in this fixture',
            })
            assert response.status_code == 201
    finally:
        app.dependency_overrides.clear()


def test_zapier_then_mailbox_reviews_actual_attachment_once(client, db_session, monkeypatch):
    from fastapi.testclient import TestClient
    from app.main import app
    from app.db import get_db
    monkeypatch.setattr(imap_service, 'imap_configured', lambda: True)
    monkeypatch.setattr(imap_service, 'start_poller', Mock())
    monkeypatch.setattr(imap_service, 'SessionLocal', TestingSessionLocal)
    monkeypatch.setattr('app.services.smtp_service.smtp_configured', lambda: False)
    monkeypatch.setenv('EMAIL_WEBHOOK_SECRET', TEST_SECRET)
    message_id = '<queued-attachment@example.com>'
    response = client.post('/api/v1/emails/incoming', headers=HEADERS, json={
        'message_id': message_id, 'sender': 'patient@example.com', 'recipient': 'support@hope.org',
        'body_plain': 'Please review the attached prescription.',
    })
    assert response.status_code == 202
    message = EmailMessage()
    message['Message-ID'] = message_id
    message['From'] = 'patient@example.com'
    message['To'] = 'support@hope.org'
    message['Subject'] = 'Medical document'
    message.set_content('Please review the attached prescription.')
    message.add_attachment(b'image-fixture', maintype='image', subtype='png', filename='prescription.png')
    analysis = Mock(return_value={'patient_name': 'Patient', 'status': 'under_review',
                                  'auto_reply_body': 'Thank you for the prescription. Please provide the hospital estimate and patient ID.'})
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', analysis)
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app, client=('127.0.0.1', 12345)) as local:
            def post(url, **kwargs):
                if url.startswith('http://127.0.0.1:'):
                    result = local.post('/api/v1/emails/incoming', headers=kwargs['headers'], json=kwargs['json'])
                    return Mock(ok=result.is_success, status_code=result.status_code, text=result.text)
                return Mock(ok=True)  # Outgoing email transport, not a second ingest.
            monkeypatch.setattr(imap_service.requests, 'post', post)
            assert imap_service._process_message(message.as_bytes()) is True
            assert imap_service._process_message(message.as_bytes()) is True
    finally:
        app.dependency_overrides.clear()
    assert analysis.call_count == 1
    assert analysis.call_args.kwargs['attachment_metadata'][0]['filename'] == 'prescription.png'
    assert analysis.call_args.kwargs['attachment_metadata'][0]['url'].startswith('https://')
    db_session.expire_all()
    row = db_session.execute(select(IncomingEmail)).scalar_one()
    assert row.raw_payload['intake_status'] == 'processed'
    assert row.attachment_count == 1
    assert db_session.execute(select(func.count()).select_from(OutgoingEmail)).scalar_one() == 1


def test_pending_mail_is_found_even_if_other_client_marked_it_read(client, db_session, monkeypatch):
    monkeypatch.setattr(imap_service, 'imap_configured', lambda: True)
    monkeypatch.setattr(imap_service, 'SessionLocal', TestingSessionLocal)
    monkeypatch.setenv('IMAP_HOST', 'test.invalid')
    monkeypatch.setenv('IMAP_USER', 'test-user')
    monkeypatch.setenv('IMAP_PASSWORD', 'test-password')
    client.post('/api/v1/emails/incoming', headers=HEADERS, json={
        'message_id': '<already-read@example.com>', 'sender': 'patient@example.com', 'recipient': 'support@hope.org',
    })
    connection = Mock()
    connection.search.side_effect = [('OK', [b'']), ('OK', [b'7'])]
    connection.fetch.return_value = ('OK', [(b'7 BODY', b'raw-message')])
    context = Mock()
    context.__enter__ = Mock(return_value=connection)
    context.__exit__ = Mock(return_value=False)
    monkeypatch.setattr(imap_service.imaplib, 'IMAP4_SSL', Mock(return_value=context))
    process = Mock(return_value=True)
    monkeypatch.setattr(imap_service, '_process_message', process)
    assert imap_service.poll_once() == 1
    process.assert_called_once_with(b'raw-message')
    assert connection.search.call_args_list[1].args == (None, 'HEADER', 'Message-ID', '"<already-read@example.com>"')
