"""add plan relations

Revision ID: add_plan_relations
Revises: add_niches_and_services
Create Date: 2024-11-21 15:55:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_plan_relations'
down_revision = 'add_niches_and_services'
branch_labels = None
depends_on = None

def upgrade():
    # Create plan_niches table
    op.create_table('plan_niches',
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('niche_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['niche_id'], ['niches.id'], ),
        sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ),
        sa.PrimaryKeyConstraint('plan_id', 'niche_id')
    )

    # Create plan_services table
    op.create_table('plan_services',
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['service_id'], ['services.id'], ),
        sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ),
        sa.PrimaryKeyConstraint('plan_id', 'service_id')
    )

def downgrade():
    # Drop plan_niches and plan_services tables
    op.drop_table('plan_services')
    op.drop_table('plan_niches')
