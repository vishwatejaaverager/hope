"""Record approval provenance; do not trust legacy AI approvals."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'a5c3e9f12b34'
down_revision = 'f4b2d8e01a23'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cases', sa.Column('approval_source', sa.String(32), nullable=True))
    op.add_column('cases', sa.Column('verification_evidence', sa.JSON().with_variant(postgresql.JSONB(), 'postgresql'), nullable=True))
    op.add_column('cases', sa.Column('verification_issues', sa.JSON().with_variant(postgresql.JSONB(), 'postgresql'), nullable=True))
    # Previous AI approvals have no evidence trail. Preserve existing payments,
    # but require a fresh verification before any new payout can be initiated.
    op.execute("UPDATE cases SET status = 'under_review', next_action = 'Recheck supporting documents before approving assistance' WHERE status = 'approved' AND NOT EXISTS (SELECT 1 FROM payouts WHERE payouts.case_id = cases.id)")


def downgrade():
    op.drop_column('cases', 'verification_issues')
    op.drop_column('cases', 'verification_evidence')
    op.drop_column('cases', 'approval_source')
