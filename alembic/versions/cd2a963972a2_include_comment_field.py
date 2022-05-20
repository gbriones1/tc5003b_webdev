"""include comment field

Revision ID: cd2a963972a2
Revises: 
Create Date: 2022-05-05 16:34:38.155770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd2a963972a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('device_type', sa.Column('comment', sa.String))


def downgrade():
    op.drop_column('device_type', 'comment')
