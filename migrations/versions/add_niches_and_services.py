"""add niches and services tables

Revision ID: add_niches_and_services
Revises: a5d8f008328a
Create Date: 2024-11-21 15:50:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_niches_and_services'
down_revision = 'a5d8f008328a'
branch_labels = None
depends_on = None

def upgrade():
    # Create niches table
    op.create_table('niches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create services table
    op.create_table('services',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create user_niches table
    op.create_table('user_niches',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('niche_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['niche_id'], ['niches.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'niche_id')
    )

    # Create user_services table
    op.create_table('user_services',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['service_id'], ['services.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'service_id')
    )

def downgrade():
    op.drop_table('user_services')
    op.drop_table('user_niches')
    op.drop_table('services')
    op.drop_table('niches')
