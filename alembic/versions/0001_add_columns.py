from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_add_columns'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('teachers', sa.Column('email', sa.String(length=255), nullable=True))
    op.add_column('subjects', sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True))


def downgrade():
    op.drop_column('subjects', 'metadata')
    op.drop_column('teachers', 'email')
