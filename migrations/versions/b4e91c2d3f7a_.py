"""Per-category read tracking and last_email_sent

Revision ID: b4e91c2d3f7a
Revises: 7a75a587ed99
Create Date: 2026-04-26 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b4e91c2d3f7a'
down_revision = '6fa46a1b8bb8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_category_reads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('last_read', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'category', name='uq_user_category_read'),
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_email_sent', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))


def downgrade():
    op.drop_table('user_category_reads')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('last_email_sent')
