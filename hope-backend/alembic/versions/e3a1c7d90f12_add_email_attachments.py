"""add email_attachments table for IMAP-downloaded documents

Revision ID: e3a1c7d90f12
Revises: d2f9b845e678
Create Date: 2026-11-09 15:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'e3a1c7d90f12'
down_revision: Union[str, Sequence[str], None] = 'd2f9b845e678'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'email_attachments',
        sa.Column('id', sa.Uuid(), primary_key=True),
        sa.Column('message_id', sa.String(255), nullable=True, index=True),
        sa.Column('filename', sa.String(500), nullable=False),
        sa.Column('content_type', sa.String(255), nullable=True),
        sa.Column('size', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('data', sa.LargeBinary(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('email_attachments')

