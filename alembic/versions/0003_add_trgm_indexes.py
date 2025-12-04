from alembic import op
import sqlalchemy as sa

revision = '0003_add_trgm_indexes'
down_revision = '0002_add_indexes'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_subjects_name_trgm ON subjects USING GIN (name gin_trgm_ops);"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_subjects_metadata_description_trgm ON subjects USING GIN ((metadata->>'description') gin_trgm_ops);"
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_subjects_metadata_description_trgm;")
    op.execute("DROP INDEX IF EXISTS ix_subjects_name_trgm;")
