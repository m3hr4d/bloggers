"""add user fields to service tickets

Revision ID: 2024_11_21_01
Revises: update_chat_and_ticket_tables
Create Date: 2024-11-21 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2024_11_21_01'
down_revision = 'update_chat_and_ticket_tables'
branch_labels = None
depends_on = None


def upgrade():
    # Add influencer_id and business_id columns to service_tickets table
    op.add_column('service_tickets', sa.Column('influencer_id', sa.Integer(), nullable=False))
    op.add_column('service_tickets', sa.Column('business_id', sa.Integer(), nullable=False))
    
    # Add foreign key constraints
    op.create_foreign_key(
        'fk_service_tickets_influencer_id_user',
        'service_tickets', 'user',
        ['influencer_id'], ['id']
    )
    op.create_foreign_key(
        'fk_service_tickets_business_id_user',
        'service_tickets', 'user',
        ['business_id'], ['id']
    )


def downgrade():
    # Remove foreign key constraints
    op.drop_constraint('fk_service_tickets_business_id_user', 'service_tickets', type_='foreignkey')
    op.drop_constraint('fk_service_tickets_influencer_id_user', 'service_tickets', type_='foreignkey')
    
    # Remove columns
    op.drop_column('service_tickets', 'business_id')
    op.drop_column('service_tickets', 'influencer_id')
