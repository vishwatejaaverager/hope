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
