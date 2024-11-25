"""Initial migration with all user columns

Revision ID: 53cb2044499a
Revises: 
Create Date: 2024-11-17 16:02:41.067046

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '53cb2044499a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('social_media_accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('platform', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('profile_url', sa.String(length=255), nullable=True),
    sa.Column('followers', sa.Integer(), nullable=True),
    sa.Column('engagement_rate', sa.Float(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('last_synced', sa.DateTime(), nullable=True),
    sa.Column('auth_token', sa.String(length=255), nullable=True),
    sa.Column('token_expiry', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_analytics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('profile_views', sa.Integer(), nullable=True),
    sa.Column('total_collaborations', sa.Integer(), nullable=True),
    sa.Column('successful_collaborations', sa.Integer(), nullable=True),
    sa.Column('response_time_avg', sa.Float(), nullable=True),
    sa.Column('last_active', sa.DateTime(), nullable=True),
    sa.Column('rating_avg', sa.Float(), nullable=True),
    sa.Column('engagement_rate', sa.Float(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_verification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('verification_type', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('verification_data', sa.JSON(), nullable=True),
    sa.Column('submitted_at', sa.DateTime(), nullable=True),
    sa.Column('verified_at', sa.DateTime(), nullable=True),
    sa.Column('verified_by', sa.Integer(), nullable=True),
    sa.Column('expiry_date', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['verified_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('portfolio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('media_type', sa.String(length=50), nullable=True),
    sa.Column('media_url', sa.String(length=255), nullable=True),
    sa.Column('collaboration_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['collaboration_id'], ['offer.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('website', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('language', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('timezone', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('verification_level', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('account_status', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('email_verified', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('phone_verified', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('two_factor_enabled', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('collaboration_types', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('preferred_categories', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('min_budget', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('availability_calendar', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('past_collaborations', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('business_registration', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('company_size', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('founded_year', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('business_description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('services_offered', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('service_locations', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('business_hours', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('campaign_preferences', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('pricing_templates', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('email_notifications', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('sms_notifications', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('new_offers_notifications', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('message_notifications', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('campaign_notifications', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('marketing_notifications', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('profile_visibility', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('show_contact_info', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('show_analytics', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('allow_messages', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('notification_preferences', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('privacy_settings', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('marketing_preferences', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_login', sa.DateTime(), nullable=True))
        batch_op.alter_column('content_needs',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.drop_column('engagement_rate')
        batch_op.drop_column('instagram_profile')
        batch_op.drop_column('followers')
        batch_op.drop_column('categories')
        batch_op.drop_column('business_website')
        batch_op.drop_column('experience_level')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('experience_level', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=True))
        batch_op.add_column(sa.Column('business_website', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=200), nullable=True))
        batch_op.add_column(sa.Column('categories', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255), nullable=True))
        batch_op.add_column(sa.Column('followers', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('instagram_profile', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100), nullable=True))
        batch_op.add_column(sa.Column('engagement_rate', mysql.FLOAT(), nullable=True))
        batch_op.alter_column('content_needs',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
               existing_nullable=True)
        batch_op.drop_column('last_login')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('marketing_preferences')
        batch_op.drop_column('privacy_settings')
        batch_op.drop_column('notification_preferences')
        batch_op.drop_column('allow_messages')
        batch_op.drop_column('show_analytics')
        batch_op.drop_column('show_contact_info')
        batch_op.drop_column('profile_visibility')
        batch_op.drop_column('marketing_notifications')
        batch_op.drop_column('campaign_notifications')
        batch_op.drop_column('message_notifications')
        batch_op.drop_column('new_offers_notifications')
        batch_op.drop_column('sms_notifications')
        batch_op.drop_column('email_notifications')
        batch_op.drop_column('pricing_templates')
        batch_op.drop_column('campaign_preferences')
        batch_op.drop_column('business_hours')
        batch_op.drop_column('service_locations')
        batch_op.drop_column('services_offered')
        batch_op.drop_column('business_description')
        batch_op.drop_column('founded_year')
        batch_op.drop_column('company_size')
        batch_op.drop_column('business_registration')
        batch_op.drop_column('past_collaborations')
        batch_op.drop_column('availability_calendar')
        batch_op.drop_column('min_budget')
        batch_op.drop_column('preferred_categories')
        batch_op.drop_column('collaboration_types')
        batch_op.drop_column('two_factor_enabled')
        batch_op.drop_column('phone_verified')
        batch_op.drop_column('email_verified')
        batch_op.drop_column('account_status')
        batch_op.drop_column('verification_level')
        batch_op.drop_column('is_verified')
        batch_op.drop_column('timezone')
        batch_op.drop_column('language')
        batch_op.drop_column('website')
        batch_op.drop_column('phone')

    op.drop_table('portfolio')
    op.drop_table('user_verification')
    op.drop_table('user_analytics')
    op.drop_table('social_media_accounts')
    # ### end Alembic commands ###