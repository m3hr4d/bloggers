"""update chat and ticket tables

Revision ID: update_chat_and_ticket_tables
Revises: 987ed6d2ae75
Create Date: 2024-11-21

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'update_chat_and_ticket_tables'
down_revision = '987ed6d2ae75'
branch_labels = None
depends_on = None

def upgrade():
    # Create conversations table
    op.create_table('conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('influencer_id', sa.Integer(), nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['business_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['influencer_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create conversation_messages association table
    op.create_table('conversation_messages',
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
        sa.PrimaryKeyConstraint('conversation_id', 'message_id')
    )

    # Create service_tickets table
    op.create_table('service_tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('service_type', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('service_tickets')
    op.drop_table('conversation_messages')
    op.drop_table('conversations')
