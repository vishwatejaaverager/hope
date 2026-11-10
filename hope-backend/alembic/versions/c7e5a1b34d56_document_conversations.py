"""Persist document records and case review history."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = 'c7e5a1b34d56'
down_revision = 'b6d4f0a23c45'
branch_labels = None
depends_on = None


def upgrade():
    json_type = sa.JSON().with_variant(postgresql.JSONB(), 'postgresql')
    op.create_table('documents',
        sa.Column('id', sa.Uuid(), primary_key=True),
        sa.Column('case_id', sa.Uuid(), sa.ForeignKey('cases.id', ondelete='SET NULL'), nullable=True),
        sa.Column('email_id', sa.Uuid(), sa.ForeignKey('incoming_emails.id', ondelete='CASCADE'), nullable=False),
        sa.Column('attachment_index', sa.Integer(), nullable=False),
        sa.Column('source_id', sa.String(64), nullable=False),
        sa.Column('filename', sa.String(500), nullable=False),
        sa.Column('file_metadata', json_type, nullable=False),
        sa.Column('document_type', sa.String(64), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('is_current', sa.Boolean(), nullable=False),
        sa.Column('extracted_data', json_type, nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('email_id', 'attachment_index', name='uq_document_email_attachment'))
    for field in ('case_id', 'email_id', 'source_id'):
        op.create_index('ix_documents_' + field, 'documents', [field])
    op.create_table('case_reviews',
        sa.Column('id', sa.Uuid(), primary_key=True),
        sa.Column('case_id', sa.Uuid(), sa.ForeignKey('cases.id', ondelete='CASCADE'), nullable=False),
        sa.Column('email_id', sa.Uuid(), sa.ForeignKey('incoming_emails.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('report', json_type, nullable=False),
        sa.Column('reply_draft', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index('ix_case_reviews_case_id', 'case_reviews', ['case_id'])


def downgrade():
    op.drop_table('case_reviews')
    op.drop_table('documents')
