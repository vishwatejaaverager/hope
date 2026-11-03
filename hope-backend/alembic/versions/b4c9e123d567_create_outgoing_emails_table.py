"""create outgoing_emails table

Revision ID: b4c9e123d567
Revises: a78d91c4e201
Create Date: 2026-11-03 16:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b4c9e123d567'
down_revision: Union[str, Sequence[str], None] = 'a78d91c4e201'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'outgoing_emails',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('application_id', sa.String(length=64), nullable=False),
        sa.Column('recipient_email', sa.String(length=255), nullable=False),
        sa.Column('subject', sa.String(length=500), nullable=False),
        sa.Column('body_plain', sa.Text(), nullable=False),
        sa.Column('body_html', sa.Text(), nullable=True),
        sa.Column('reply_to_message_id', sa.String(length=255), nullable=True),
        sa.Column('correlation_id', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='pending'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('raw_payload', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_outgoing_emails_application_id'), 'outgoing_emails', ['application_id'], unique=False)
    op.create_index(op.f('ix_outgoing_emails_reply_to_message_id'), 'outgoing_emails', ['reply_to_message_id'], unique=False)
    op.create_index(op.f('ix_outgoing_emails_correlation_id'), 'outgoing_emails', ['correlation_id'], unique=False)
    op.create_index(op.f('ix_outgoing_emails_status'), 'outgoing_emails', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_outgoing_emails_status'), table_name='outgoing_emails')
    op.drop_index(op.f('ix_outgoing_emails_correlation_id'), table_name='outgoing_emails')
    op.drop_index(op.f('ix_outgoing_emails_reply_to_message_id'), table_name='outgoing_emails')
    op.drop_index(op.f('ix_outgoing_emails_application_id'), table_name='outgoing_emails')
    op.drop_table('outgoing_emails')
