"""create incoming_emails table

Revision ID: a78d91c4e201
Revises: f30dcfe93533
Create Date: 2026-11-03 14:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a78d91c4e201'
down_revision: Union[str, Sequence[str], None] = 'f30dcfe93533'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'incoming_emails',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('message_id', sa.String(length=255), nullable=False),
        sa.Column('sender', sa.String(length=255), nullable=False),
        sa.Column('recipient', sa.String(length=255), nullable=False),
        sa.Column('subject', sa.String(length=500), nullable=True),
        sa.Column('body_plain', sa.Text(), nullable=True),
        sa.Column('body_html', sa.Text(), nullable=True),
        sa.Column('attachment_metadata', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=True),
        sa.Column('attachment_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('application_id', sa.String(length=64), nullable=True),
        sa.Column('raw_payload', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=True),
        sa.Column('received_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('message_id', name='uq_incoming_emails_message_id')
    )
    op.create_index(op.f('ix_incoming_emails_application_id'), 'incoming_emails', ['application_id'], unique=False)
    op.create_index(op.f('ix_incoming_emails_message_id'), 'incoming_emails', ['message_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_incoming_emails_message_id'), table_name='incoming_emails')
    op.drop_index(op.f('ix_incoming_emails_application_id'), table_name='incoming_emails')
    op.drop_table('incoming_emails')
