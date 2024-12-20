"""Re-add followers_count to User model

Revision ID: 987ed6d2ae75
Revises: 35ade03fb51f
Create Date: 2024-11-17 16:07:15.019190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '987ed6d2ae75'
down_revision = '35ade03fb51f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('followers_count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('followers_count')

    # ### end Alembic commands ###
