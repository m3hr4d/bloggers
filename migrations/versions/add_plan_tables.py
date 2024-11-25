"""add plan tables

Revision ID: add_plan_tables
Revises: add_plan_relations
Create Date: 2024-11-21 15:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_plan_tables'
down_revision = 'add_plan_relations'
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

    # Add new columns to plan table
    op.add_column('plan', sa.Column('title', sa.String(length=100), nullable=True))
    op.add_column('plan', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('plan', sa.Column('available_times', sa.JSON(), nullable=True))
    op.add_column('plan', sa.Column('content_suggestions', sa.Text(), nullable=True))
    op.add_column('plan', sa.Column('suggested_price', sa.Float(), nullable=True))
    op.add_column('plan', sa.Column('additional_notes', sa.Text(), nullable=True))
    op.add_column('plan', sa.Column('custom_services', sa.JSON(), nullable=True))
    op.add_column('plan', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('plan', sa.Column('updated_at', sa.DateTime(), nullable=True))

    # Change start_date and end_date columns to DateTime
    op.alter_column('plan', 'start_date',
        existing_type=sa.String(length=100),
        type_=sa.DateTime(),
        existing_nullable=True)
    op.alter_column('plan', 'end_date',
        existing_type=sa.String(length=100),
        type_=sa.DateTime(),
        existing_nullable=True)

def downgrade():
    # Drop plan_niches and plan_services tables
    op.drop_table('plan_niches')
    op.drop_table('plan_services')

    # Drop new columns from plan table
    op.drop_column('plan', 'updated_at')
    op.drop_column('plan', 'created_at')
    op.drop_column('plan', 'custom_services')
    op.drop_column('plan', 'additional_notes')
    op.drop_column('plan', 'suggested_price')
    op.drop_column('plan', 'content_suggestions')
    op.drop_column('plan', 'available_times')
    op.drop_column('plan', 'description')
    op.drop_column('plan', 'title')

    # Change start_date and end_date columns back to String
    op.alter_column('plan', 'start_date',
        existing_type=sa.DateTime(),
        type_=sa.String(length=100),
        existing_nullable=True)
    op.alter_column('plan', 'end_date',
        existing_type=sa.DateTime(),
        type_=sa.String(length=100),
        existing_nullable=True)
