"""Add followers_count to User model

Revision ID: 4d9cebfd638c
Revises: 53cb2044499a
Create Date: 2024-11-17 16:04:16.371167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d9cebfd638c'
down_revision = '53cb2044499a'
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