"""Store the AI review decision, evidence references, and red flags."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = 'b6d4f0a23c45'
down_revision = 'a5c3e9f12b34'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cases', sa.Column('review_report', sa.JSON().with_variant(postgresql.JSONB(), 'postgresql'), nullable=True))


def downgrade():
    op.drop_column('cases', 'review_report')
