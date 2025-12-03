from alembic import op
import sqlalchemy as sa

revision = '0002_add_indexes'
down_revision = '0001_add_columns'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('ix_teachers_full_name', 'teachers', ['full_name'], unique=False)
    op.create_index('ix_lessons_date_time', 'lessons', ['date', 'time'], unique=False)


def downgrade():
    op.drop_index('ix_lessons_date_time', table_name='lessons')
    op.drop_index('ix_teachers_full_name', table_name='teachers')
