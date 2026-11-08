"""add email_exchanges to cases and drop ai_summary from incoming_emails

Revision ID: d2f9b845e678
Revises: c1e8a934d567
Create Date: 2026-11-08 14:22:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd2f9b845e678'
down_revision: Union[str, Sequence[str], None] = 'c1e8a934d567'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'cases',
        sa.Column(
            'email_exchanges',
            sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'),
            nullable=True,
        ),
    )
    op.drop_column('incoming_emails', 'ai_summary')


def downgrade() -> None:
    op.add_column(
        'incoming_emails',
        sa.Column(
            'ai_summary',
            sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'),
            nullable=True,
        ),
    )
    op.drop_column('cases', 'email_exchanges')

