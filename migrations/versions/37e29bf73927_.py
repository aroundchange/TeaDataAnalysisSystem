from alembic import op
import sqlalchemy as sa

revision = '37e29bf73927'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('recommend',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('image', sa.Text(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('recommend')

