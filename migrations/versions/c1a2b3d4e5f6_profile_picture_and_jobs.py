"""profile picture and scheduled jobs

Revision ID: c1a2b3d4e5f6
Revises: b4e91c2d3f7a
Create Date: 2026-05-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'c1a2b3d4e5f6'
down_revision = 'b4e91c2d3f7a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=256), nullable=True))

    op.create_table(
        'scheduled_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('last_run', sa.DateTime(), nullable=True),
        sa.Column('interval_minutes', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )


def downgrade():
    op.drop_table('scheduled_jobs')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('profile_picture')
