"""add mail subscriptions

Revision ID: a1b2c3d4e5f6
Revises: 2568f6497425
Create Date: 2026-04-25 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f6'
down_revision = '929dec5f7754'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('mail_subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('send_days', sa.String(length=20), nullable=False, server_default='0,1,2,3,4,5,6'),
        sa.Column('send_hour', sa.Integer(), nullable=False, server_default='8'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_table('mail_blocks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subscription_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('post_count', sa.Integer(), nullable=False, server_default='2'),
        sa.ForeignKeyConstraint(['subscription_id'], ['mail_subscriptions.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('mail_blocks')
    op.drop_table('mail_subscriptions')
