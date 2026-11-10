"""Resolve stored email files and merge richer deliveries without reprocessing a case."""
import os
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import EmailAttachment


def normalize(items: Any) -> list[dict]:
    result = []
    for item in items if isinstance(items, list) else []:
        item = item.model_dump(exclude_none=True) if hasattr(item, 'model_dump') else item
        if not isinstance(item, dict):
            continue
        doc = dict(item)
        doc['url'] = doc.get('url') or doc.get('attachment_url') or doc.get('file_url') or doc.get('file')
        doc['filename'] = doc.get('filename') or doc.get('name') or 'Attached document'
        result.append(doc)
    return result


def merge(existing: Any, incoming: Any) -> list[dict]:
    documents = normalize(existing)
    for doc in normalize(incoming):
        url = str(doc.get('url') or '')
        internal = '/api/v1/emails/attachments/' in url
        match = None
        for index, previous in enumerate(documents):
            old_url = str(previous.get('url') or '')
            same_name = previous.get('filename') == doc.get('filename')
            if (url.startswith(('http://', 'https://')) and url == old_url) or (same_name and not old_url.startswith(('http://', 'https://'))):
                match = index
                break
            if same_name and internal and '/api/v1/emails/attachments/' not in old_url:
                match = index
                break
            if same_name and not internal and '/api/v1/emails/attachments/' in old_url:
                match = index
                doc = {**doc, **previous}
                break
        if match is None:
            documents.append(doc)
        else:
            documents[match] = {**documents[match], **doc}
    return documents


def stored_metadata(db: Session, message_ids: list[str]) -> dict[str, list[dict]]:
    if not message_ids:
        return {}
    base = os.getenv('PUBLIC_BASE_URL', 'https://hope-9dq5.onrender.com').rstrip('/')
    # Select metadata only; dashboard reads must not load all binary documents.
    rows = db.execute(select(EmailAttachment.message_id, EmailAttachment.id, EmailAttachment.filename,
                             EmailAttachment.content_type, EmailAttachment.size)
                      .where(EmailAttachment.message_id.in_(message_ids))).all()
    result: dict[str, list[dict]] = {}
    for row in rows:
        result.setdefault(row.message_id, []).append({
            'filename': row.filename, 'content_type': row.content_type, 'size': row.size,
            'url': f'{base}/api/v1/emails/attachments/{row.id}',
        })
    return result
