"""create cases table and case linkages

Revision ID: c1e8a934d567
Revises: b4c9e123d567
Create Date: 2026-11-07 23:08:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c1e8a934d567'
down_revision: Union[str, Sequence[str], None] = 'b4c9e123d567'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create cases table
    op.create_table(
        'cases',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('case_number', sa.String(length=32), nullable=False),
        sa.Column('patient_user_id', sa.String(length=64), nullable=True),
        sa.Column('patient_name', sa.String(length=255), nullable=True),
        sa.Column('patient_email', sa.String(length=255), nullable=True),
        sa.Column('medical_category', sa.String(length=64), nullable=True),
        sa.Column('treatment_description', sa.Text(), nullable=True),
        sa.Column('hospital_name', sa.String(length=255), nullable=True),
        sa.Column('estimated_cost', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('requested_amount', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='USD'),
        sa.Column('urgency', sa.String(length=32), nullable=False, server_default='medium'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='new'),
        sa.Column('overall_summary', sa.Text(), nullable=True),
        sa.Column('next_action', sa.String(length=255), nullable=True),
        sa.Column('pending_items', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('case_number', name='uq_cases_case_number')
    )
    op.create_index(op.f('ix_cases_case_number'), 'cases', ['case_number'], unique=True)
    op.create_index(op.f('ix_cases_patient_email'), 'cases', ['patient_email'], unique=False)
    op.create_index(op.f('ix_cases_medical_category'), 'cases', ['medical_category'], unique=False)
    op.create_index(op.f('ix_cases_status'), 'cases', ['status'], unique=False)

    # 2. Add case_id and ai_summary to incoming_emails
    op.add_column('incoming_emails', sa.Column('case_id', sa.Uuid(), nullable=True))
    op.add_column('incoming_emails', sa.Column('ai_summary', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=True))
    op.create_index(op.f('ix_incoming_emails_case_id'), 'incoming_emails', ['case_id'], unique=False)
    op.create_foreign_key('fk_incoming_emails_case_id', 'incoming_emails', 'cases', ['case_id'], ['id'], ondelete='SET NULL')

    # 3. Add case_id to outgoing_emails
    op.add_column('outgoing_emails', sa.Column('case_id', sa.Uuid(), nullable=True))
    op.create_index(op.f('ix_outgoing_emails_case_id'), 'outgoing_emails', ['case_id'], unique=False)
    op.create_foreign_key('fk_outgoing_emails_case_id', 'outgoing_emails', 'cases', ['case_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    # Drop outgoing_emails linkages
    op.drop_constraint('fk_outgoing_emails_case_id', 'outgoing_emails', type_='foreignkey')
    op.drop_index(op.f('ix_outgoing_emails_case_id'), table_name='outgoing_emails')
    op.drop_column('outgoing_emails', 'case_id')

    # Drop incoming_emails linkages
    op.drop_constraint('fk_incoming_emails_case_id', 'incoming_emails', type_='foreignkey')
    op.drop_index(op.f('ix_incoming_emails_case_id'), table_name='incoming_emails')
    op.drop_column('incoming_emails', 'ai_summary')
    op.drop_column('incoming_emails', 'case_id')

    # Drop cases table
    op.drop_index(op.f('ix_cases_status'), table_name='cases')
    op.drop_index(op.f('ix_cases_medical_category'), table_name='cases')
    op.drop_index(op.f('ix_cases_patient_email'), table_name='cases')
    op.drop_index(op.f('ix_cases_case_number'), table_name='cases')
    op.drop_table('cases')
