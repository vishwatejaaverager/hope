from copy import deepcopy
from unittest.mock import Mock
from sqlalchemy import select
from app.models import Case, CaseDocument, CaseReview, IncomingEmail, Payout
from app.services import ai_service, case_review
from app.api.routes.email import _resolve_case
from tests.test_case_payment_flow import client, db_session, setup_database, isolate, TEST_SECRET
from tests.test_case_review import report, attachments


def submit(client, message_id, documents, **fields):
    return client.post('/api/v1/emails/incoming', headers={'X-Webhook-Secret': TEST_SECRET}, json={
        'message_id': message_id, 'sender': 'patient@example.com', 'recipient': 'support@hope.org',
        'body_plain': 'Please review the updated evidence.',
        'attachment_metadata': [{**doc, 'url': 'https://example.com/' + doc['filename']} for doc in documents], **fields})


def flagged():
    value = report()
    value['red_flags'] = [{'message': 'The estimate is expired.', 'attachment_indexes': [1],
                           'required_action': 'Provide a current hospital estimate.'}]
    value['review_decision'] = 'request_information'
    return value


def test_omitting_prior_red_flag_cannot_clear_it():
    first = case_review.evaluate(flagged(), attachments())
    followup = report()
    followup['document_checks'] = []
    second = case_review.evaluate(followup, [], first['verification_evidence'], first['review_report'], 'Any update?')
    assert second['status'] == 'under_review'
    assert any(flag['message'] == 'The estimate is expired.' for flag in second['review_report']['red_flags'])


def test_unsupported_resolution_is_rejected():
    first = case_review.evaluate(flagged(), attachments())
    followup = report()
    followup['document_checks'] = []
    followup['resolved_red_flags'] = [{'flag_id': first['review_report']['red_flags'][0]['id'],
                                     'reason': 'All fine.', 'attachment_indexes': [99], 'email_excerpt': 'not in email'}]
    second = case_review.evaluate(followup, [], first['verification_evidence'], first['review_report'], 'Any update?')
    assert second['review_report']['resolved_red_flags'] == []
    assert second['status'] == 'under_review'


def test_quoted_history_is_not_new_confirmation():
    first = case_review.evaluate(flagged(), attachments())
    followup = report()
    followup['document_checks'] = []
    followup['resolved_red_flags'] = [{'flag_id': first['review_report']['red_flags'][0]['id'],
                                     'reason': 'Confirmed.', 'email_excerpt': 'The estimate is current.'}]
    second = case_review.evaluate(followup, [], first['verification_evidence'], first['review_report'],
                                  'Any update?\n> The estimate is current.')
    assert second['review_report']['resolved_red_flags'] == []


def test_old_concern_id_cannot_be_rewritten():
    first = case_review.evaluate(flagged(), attachments())
    followup = report()
    followup['document_checks'] = []
    followup['red_flags'] = [{'id': first['review_report']['red_flags'][0]['id'], 'message': 'Everything is okay.'}]
    second = case_review.evaluate(followup, [], first['verification_evidence'], first['review_report'])
    assert any(flag['message'] == 'The estimate is expired.' for flag in second['review_report']['red_flags'])


def test_followup_resolves_old_issue_finds_new_issue_and_preserves_history(client, db_session, monkeypatch):
    model = Mock(return_value=flagged())
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', model)
    first = submit(client, '<first@example.com>', attachments())
    assert first.status_code == 201
    case = db_session.execute(select(Case)).scalar_one()
    first_report = deepcopy(case.review_report)
    first_evidence = deepcopy(case.verification_evidence)
    old_id = next(flag['id'] for flag in first_report['red_flags'] if flag['message'] == 'The estimate is expired.')
    id_source = next(item['source_id'] for item in first_evidence if item['document_type'] == 'government_id')
    assert len(db_session.execute(select(CaseDocument)).scalars().all()) == 3

    replacement = report()
    replacement['document_checks'] = [{**report()['document_checks'][1], 'attachment_index': 0}]
    replacement['resolved_red_flags'] = [{'flag_id': old_id, 'reason': 'The replacement estimate has a current validity date.',
                                         'attachment_indexes': [0]}]
    replacement['red_flags'] = [{'message': 'The replacement estimate names a different patient.', 'source_ids': [id_source],
                                 'attachment_indexes': [0], 'required_action': 'Provide matching patient documents.'}]
    model.return_value = replacement
    second = submit(client, '<second@example.com>', [{'filename': 'new-estimate.png'}], references='<first@example.com>')
    assert second.status_code == 201
    assert second.json()['case_id'] == first.json()['case_id']
    context = model.call_args.kwargs['existing_case_context']
    assert context['review_report'] == first_report
    assert len(context['documents']) == 3
    assert any(message['direction'] == 'outgoing' for message in context['recent_messages'])
    db_session.refresh(case)
    assert case.status == 'under_review'
    assert case.review_report['resolved_red_flags'][0]['id'] == old_id
    assert any('different patient' in flag['message'] for flag in case.review_report['red_flags'])
    assert case.review_report['document_statuses']['government_id']['status'] == 'needs_review'
    documents = db_session.execute(select(CaseDocument)).scalars().all()
    assert len(documents) == 4
    old_estimate = next(doc for doc in documents if doc.source_id == first_evidence[1]['source_id'])
    assert old_estimate.is_current is False
    snapshots = db_session.execute(select(CaseReview).order_by(CaseReview.created_at)).scalars().all()
    assert len(snapshots) == 2
    assert snapshots[0].report == first_report
    assert not db_session.execute(select(Payout)).scalars().all()

    detail = client.get('/api/v1/cases/' + str(case.id), headers={'X-Webhook-Secret': TEST_SECRET}).json()
    assert len(detail['documents']) == 4
    assert len(detail['reviews']) == 2
    # Duplicate delivery must not add a second review/document/payout.
    submit(client, '<second@example.com>', [{'filename': 'new-estimate.png'}])
    assert len(db_session.execute(select(CaseReview)).scalars().all()) == 2
    assert model.call_count == 2

    # A later correction can resolve the new mismatch and complete the case.
    correction = report()
    correction['document_checks'] = [{**report()['document_checks'][0], 'attachment_index': 0}]
    concern = next(flag for flag in case.review_report['red_flags'] if 'different patient' in flag['message'])
    correction['resolved_red_flags'] = [{'flag_id': concern['id'], 'reason': 'The corrected identity document matches the replacement estimate.', 'attachment_indexes': [0]}]
    estimate_source = next(item['source_id'] for item in case.verification_evidence if item['document_type'] == 'cost_estimate')
    correction['previous_document_updates'] = [{'source_id': estimate_source, 'status': 'approved', 'red_flags': [],
                                               'reason': 'Patient identity is now consistent.', 'attachment_indexes': [0]}]
    model.return_value = correction
    third = submit(client, '<third@example.com>', [{'filename': 'corrected-id.png'}], references='<first@example.com> <second@example.com>')
    assert third.status_code == 201
    db_session.refresh(case)
    assert case.status == 'approved'
    assert case.review_report['red_flags'] == []
    assert len(db_session.execute(select(CaseReview)).scalars().all()) == 3


def test_approved_file_can_be_reopened_and_resolved_by_new_confirmation():
    first = case_review.evaluate(report(), attachments())
    source = first['verification_evidence'][0]['source_id']
    followup = report()
    followup['document_checks'] = []
    followup['red_flags'] = [{'message': 'Clarify the name spelling.', 'source_ids': [source]}]
    second = case_review.evaluate(followup, [], first['verification_evidence'], first['review_report'])
    assert second['review_report']['document_statuses']['government_id']['status'] == 'needs_review'
    answer = 'The hospital confirms the abbreviated name refers to Test Patient.'
    third = report()
    third['document_checks'] = []
    third['resolved_red_flags'] = [{'flag_id': second['review_report']['red_flags'][0]['id'],
                                   'reason': 'The clarification resolves the spelling concern.', 'email_excerpt': answer}]
    third['previous_document_updates'] = [{'source_id': source, 'status': 'approved', 'red_flags': [],
                                          'reason': 'Identity consistency clarified.', 'email_excerpt': answer}]
    final = case_review.evaluate(third, [], second['verification_evidence'], second['review_report'], answer)
    assert final['status'] == 'approved'


def test_documents_are_stored_before_model_call(client, db_session, monkeypatch):
    def analyze(**kwargs):
        documents = db_session.execute(select(CaseDocument)).scalars().all()
        assert len(documents) == 3
        assert all(doc.email_id and doc.case_id for doc in documents)
        assert all(doc.status == 'pending' for doc in documents)
        return report()
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', analyze)
    assert submit(client, 'stored-before-analysis', attachments()).status_code == 201


def test_provider_failure_preserves_document_and_records_failed_attempt(client, db_session, monkeypatch):
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value=ai_service._analysis_failure('patient@example.com', None, 'all_models_failed')))
    assert submit(client, 'failed-analysis', attachments()[:1]).status_code == 201
    document = db_session.execute(select(CaseDocument)).scalar_one()
    assert document.status == 'analysis_failed'
    assert db_session.execute(select(CaseReview)).scalar_one().report['analysis_status'] == 'failed'
    assert db_session.execute(select(Case)).scalar_one().status == 'under_review'


def test_ambiguous_contact_does_not_select_latest_patient(db_session):
    first = Case(case_number='ONE', patient_email='shared@example.com', patient_name='One')
    second = Case(case_number='TWO', patient_email='shared@example.com', patient_name='Two')
    db_session.add_all([first, second]); db_session.commit()
    assert _resolve_case(db_session, sender_email='shared@example.com') is None
    assert _resolve_case(db_session, app_id='ONE', sender_email='shared@example.com').id == first.id


def test_thread_reference_selects_correct_case_even_for_shared_contact(db_session):
    from datetime import datetime, timezone
    first = Case(case_number='ONE', patient_email='shared@example.com')
    second = Case(case_number='TWO', patient_email='shared@example.com')
    db_session.add_all([first, second]); db_session.flush()
    db_session.add(IncomingEmail(case_id=first.id, message_id='<original@example.com>', sender='shared@example.com',
                                  recipient='hope@example.com', received_at=datetime.now(timezone.utc)))
    db_session.commit()
    assert _resolve_case(db_session, sender_email='shared@example.com', thread_references=['<original@example.com>']).id == first.id


def test_retry_resumes_durable_intake_after_unexpected_failure(client, db_session, monkeypatch):
    import pytest
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(side_effect=RuntimeError('interrupted provider')))
    with pytest.raises(RuntimeError):
        submit(client, 'interrupted-review', attachments())
    assert len(db_session.execute(select(CaseDocument)).scalars().all()) == 3
    assert db_session.execute(select(IncomingEmail)).scalar_one().raw_payload['intake_status'] == 'review_pending'
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value=report()))
    assert submit(client, 'interrupted-review', attachments()).status_code == 201
    assert len(db_session.execute(select(CaseDocument)).scalars().all()) == 3
    assert len(db_session.execute(select(CaseReview)).scalars().all()) == 1


def test_failed_followup_suspends_automatic_approval(client, db_session, monkeypatch):
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value=report()))
    assert submit(client, 'initial-approved', attachments()).status_code == 201
    case = db_session.execute(select(Case)).scalar_one()
    assert case.status == 'approved'
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value=ai_service._analysis_failure('patient@example.com', None, 'all_models_failed')))
    assert submit(client, 'new-evidence-failed', [{'filename': 'replacement.png'}]).status_code == 201
    db_session.refresh(case)
    assert case.status == 'under_review'
    assert case.approval_source is None
    assert not db_session.execute(select(Payout)).scalars().all()


def test_inaccessible_document_cannot_pass_even_if_model_claims_readable():
    result = case_review.evaluate(report(), [{'filename': kind + '.pdf', 'content_type': 'application/pdf',
                                             'url': 'https://example.com/' + kind + '.pdf'} for kind in case_review.REQUIRED_DOCUMENTS])
    assert result['status'] == 'under_review'
    assert all(item['readable'] is False for item in result['verification_evidence'])


def test_pdf_extracted_text_can_supply_readable_evidence():
    result = case_review.evaluate(report(), [{'filename': kind + '.pdf', 'content_type': 'application/pdf',
                                             'extracted_text': 'Extracted patient document text.'} for kind in case_review.REQUIRED_DOCUMENTS])
    assert result['status'] == 'approved'


def test_pending_submission_prevents_new_payout(db_session):
    from datetime import datetime, timezone
    from app.services import case_workflow
    value = case_review.evaluate(report(), attachments())
    case = Case(case_number='PENDING-REVIEW', patient_email='patient@example.com', status='approved',
                approval_source=case_review.APPROVAL_SOURCE, review_report=value['review_report'])
    db_session.add(case); db_session.flush()
    db_session.add(IncomingEmail(case_id=case.id, message_id='pending-evidence', sender='patient@example.com',
                                recipient='hope@example.com', received_at=datetime.now(timezone.utc),
                                raw_payload={'intake_status': 'review_pending'}))
    db_session.commit()
    assert 'awaiting review' in case_workflow.process_approved_case(db_session, case)
    assert case.status == 'under_review'
    assert not db_session.execute(select(Payout)).scalars().all()


def test_document_verdict_saved_and_flags_appear_in_reply(client, db_session, monkeypatch):
    value = report()
    messages = ['Line items total $20,000 but printed total is $18,000.',
                'Printed dates span 31 days but stated validity is 30 days.']
    for index, check in enumerate(value['document_checks']):
        check.pop('status')
        check.pop('red_flags')
        check.update(is_verified=index != 1, flags=messages if index == 1 else [])
    value['review_decision'] = 'request_information'
    value['auto_reply_body'] = 'Thanks for sending your estimate. ' + ' '.join(messages) + ' Could you send a corrected copy?'
    monkeypatch.setattr(ai_service, 'analyze_incoming_email', Mock(return_value=value))
    response = submit(client, 'document-verdicts', attachments())
    assert response.status_code == 201
    reply = response.json()['auto_reply_body']
    assert reply == value['auto_reply_body']
    documents = {doc.document_type: doc for doc in db_session.execute(select(CaseDocument)).scalars()}
    assert documents['government_id'].status == 'verified'
    assert documents['government_id'].extracted_data['is_verified'] is True
    assert documents['cost_estimate'].status == 'needs_review'
    assert documents['cost_estimate'].extracted_data['flags'] == messages
    assert db_session.execute(select(Case)).scalar_one().status == 'under_review'
    assert not db_session.execute(select(Payout)).scalars().all()
