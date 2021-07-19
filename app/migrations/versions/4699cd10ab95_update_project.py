"""Update Project

Revision ID: 4699cd10ab95
Revises: 9c40cf9cfd4e
Create Date: 2021-07-07 12:37:02.926672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4699cd10ab95'
down_revision = '9c40cf9cfd4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('create', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'create')
    # ### end Alembic commands ###