"""Store confirmed PayPal address and enforce one payout per case."""
from alembic import op
import sqlalchemy as sa

revision = 'f4b2d8e01a23'
down_revision = 'e3a1c7d90f12'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cases', sa.Column('paypal_email', sa.String(255), nullable=True))
    op.add_column('payouts', sa.Column('case_id', sa.Uuid(), nullable=True))
    op.create_foreign_key('fk_payout_case', 'payouts', 'cases', ['case_id'], ['id'])
    op.create_unique_constraint('uq_payout_case', 'payouts', ['case_id'])


def downgrade():
    op.drop_constraint('uq_payout_case', 'payouts', type_='unique')
    op.drop_constraint('fk_payout_case', 'payouts', type_='foreignkey')
    op.drop_column('payouts', 'case_id')
    op.drop_column('cases', 'paypal_email')
