"""initial migrate

Revision ID: 9c40cf9cfd4e
Revises: 
Create Date: 2021-07-06 18:56:44.728566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c40cf9cfd4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('surname', sa.String(length=100), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('position', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('avatar', sa.LargeBinary(), nullable=True),
    sa.Column('slug', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('describe', sa.Text(), nullable=True),
    sa.Column('slug', sa.String(length=140), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manager_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('project_executors',
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('describe', sa.Text(), nullable=True),
    sa.Column('date_begin', sa.Date(), nullable=True),
    sa.Column('date_end', sa.Date(), nullable=True),
    sa.Column('task_type', sa.String(length=20), nullable=True),
    sa.Column('priority', sa.String(length=20), nullable=True),
    sa.Column('num_of_hours', sa.Integer(), nullable=True),
    sa.Column('slug', sa.String(length=120), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manager_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('journal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_spent', sa.DateTime(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks_executors',
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('journal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['journal_id'], ['journal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('tasks_executors')
    op.drop_table('journal')
    op.drop_table('task')
    op.drop_table('project_executors')
    op.drop_table('roles_users')
    op.drop_table('project')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###