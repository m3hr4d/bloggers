from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from email_func_app.extensions import db, login_manager
from email_func_app.models.niche import user_niches, user_services
import re

class UserVerification(db.Model):
    """Model for storing user verification details."""
    __tablename__ = 'user_verification'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    verification_type = db.Column(db.String(50), nullable=False)  # 'social_media', 'business', 'identity'
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    verification_data = db.Column(db.JSON)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    expiry_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)

class UserAnalytics(db.Model):
    """Model for storing user profile analytics."""
    __tablename__ = 'user_analytics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile_views = db.Column(db.Integer, default=0)
    total_collaborations = db.Column(db.Integer, default=0)
    successful_collaborations = db.Column(db.Integer, default=0)
    response_time_avg = db.Column(db.Float)  # in hours
    last_active = db.Column(db.DateTime)
    rating_avg = db.Column(db.Float)
    engagement_rate = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SocialMediaAccount(db.Model):
    """Model for storing linked social media accounts."""
    __tablename__ = 'social_media_accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # instagram, twitter, tiktok, etc.
    username = db.Column(db.String(100))
    profile_url = db.Column(db.String(255))
    followers = db.Column(db.Integer)
    engagement_rate = db.Column(db.Float)
    is_verified = db.Column(db.Boolean, default=False)
    last_synced = db.Column(db.DateTime)
    auth_token = db.Column(db.String(255))
    token_expiry = db.Column(db.DateTime)

class Portfolio(db.Model):
    """Model for storing user portfolio items."""
    __tablename__ = 'portfolio'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    media_type = db.Column(db.String(50))  # image, video, link
    media_url = db.Column(db.String(255))
    collaboration_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    """User model for storing user details."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    
    # Basic Information
    name = db.Column(db.String(100))
    profile_image = db.Column(db.String(255))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    language = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(50))
    instagram_profile = db.Column(db.String(255))
    followers_count = db.Column(db.Integer, default=0)
    followers = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    business_website = db.Column(db.String(255))
    
    # Verification and Status
    is_verified = db.Column(db.Boolean, default=False)
    verification_level = db.Column(db.Integer, default=0)  # 0=none, 1=basic, 2=advanced, 3=premium
    account_status = db.Column(db.String(20), default='active')  # active, suspended, inactive
    email_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    
    # Influencer Specific
    niche = db.Column(db.String(100))
    interests = db.Column(db.Text)
    collaboration_types = db.Column(db.String(255))  # Comma-separated list
    preferred_categories = db.Column(db.String(255))  # Comma-separated list
    min_budget = db.Column(db.Float)
    availability_calendar = db.Column(db.JSON)  # Store calendar data as JSON
    past_collaborations = db.Column(db.Integer, default=0)
    
    # Business Specific
    business_name = db.Column(db.String(100))
    business_registration = db.Column(db.String(100))
    business_type = db.Column(db.String(50))
    industry = db.Column(db.String(50))
    company_size = db.Column(db.String(50))
    founded_year = db.Column(db.Integer)
    business_description = db.Column(db.Text)
    services_offered = db.Column(db.Text)
    service_locations = db.Column(db.String(255))
    business_hours = db.Column(db.JSON)
    
    # Campaign and Budget
    content_needs = db.Column(db.String(255))
    annual_budget = db.Column(db.String(20))
    campaign_preferences = db.Column(db.JSON)
    pricing_templates = db.Column(db.JSON)
    
    # Notification Preferences
    email_notifications = db.Column(db.Boolean, default=True)
    sms_notifications = db.Column(db.Boolean, default=False)
    new_offers_notifications = db.Column(db.Boolean, default=True)
    message_notifications = db.Column(db.Boolean, default=True)
    campaign_notifications = db.Column(db.Boolean, default=True)
    marketing_notifications = db.Column(db.Boolean, default=True)
    
    # Privacy Settings
    profile_visibility = db.Column(db.String(20), default='public')
    show_contact_info = db.Column(db.Boolean, default=True)
    show_analytics = db.Column(db.Boolean, default=True)
    allow_messages = db.Column(db.Boolean, default=True)
    
    # Settings and Preferences
    notification_preferences = db.Column(db.JSON)
    privacy_settings = db.Column(db.JSON)
    marketing_preferences = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    onboarding_completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    verifications = db.relationship('UserVerification', foreign_keys='UserVerification.user_id', backref='user', lazy='dynamic')
    analytics = db.relationship('UserAnalytics', backref='user', uselist=False)
    social_accounts = db.relationship('SocialMediaAccount', backref='user', lazy='dynamic')
    portfolio_items = db.relationship('Portfolio', backref='user', lazy='dynamic')
    plans = db.relationship('Plan', foreign_keys='Plan.influencer_id', backref='influencer', lazy='dynamic')
    business_offers = db.relationship('Offer', foreign_keys='Offer.business_id', backref='business', lazy='dynamic')
    
    # Niche and Service relationships
    niches = db.relationship('Niche', secondary=user_niches, lazy='dynamic',
                         backref=db.backref('users', lazy='dynamic'))
    services = db.relationship('Service', secondary=user_services, lazy='dynamic',
                          backref=db.backref('users', lazy='dynamic'))
    
    # Chat relationships
    influencer_conversations = db.relationship('Conversation', foreign_keys='Conversation.influencer_id', lazy='dynamic')
    business_conversations = db.relationship('Conversation', foreign_keys='Conversation.business_id', lazy='dynamic')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', lazy='dynamic')
    
    # Service ticket relationships
    influencer_tickets = db.relationship('ServiceTicket', foreign_keys='ServiceTicket.influencer_id', lazy='dynamic')
    business_tickets = db.relationship('ServiceTicket', foreign_keys='ServiceTicket.business_id', lazy='dynamic')

    def __init__(self, email, password, user_type):
        self.email = email
        self.password = generate_password_hash(password)
        self.user_type = user_type
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def check_password(self, password):
        """Check if provided password matches the hash."""
        return check_password_hash(self.password, password)

    def is_influencer(self):
        """Check if user is an influencer."""
        return self.user_type == 'influencer'

    def is_business(self):
        """Check if user is a business."""
        return self.user_type == 'business'

    def is_admin(self):
        """Check if user is an admin."""
        return self.user_type == 'admin'

    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def get_verification_status(self):
        """Get the current verification status."""
        return {
            'is_verified': self.is_verified,
            'level': self.verification_level,
            'email_verified': self.email_verified,
            'phone_verified': self.phone_verified
        }

    def get_social_stats(self):
        """Get aggregated social media statistics."""
        stats = {
            'total_followers': 0,
            'avg_engagement': 0.0,
            'platforms': []
        }
        accounts = self.social_accounts.all()
        if accounts:
            stats['total_followers'] = sum(acc.followers or 0 for acc in accounts)
            engagement_rates = [acc.engagement_rate for acc in accounts if acc.engagement_rate]
            if engagement_rates:
                stats['avg_engagement'] = sum(engagement_rates) / len(engagement_rates)
            stats['platforms'] = [{'platform': acc.platform, 
                                 'followers': acc.followers,
                                 'engagement': acc.engagement_rate} 
                                for acc in accounts]
        return stats

    def get_analytics(self):
        """Get user analytics data."""
        if not self.analytics:
            self.analytics = UserAnalytics(user_id=self.id)
            db.session.add(self.analytics)
            db.session.commit()
        return self.analytics

    def update_profile(self, data):
        """Update user profile with provided data."""
        allowed_fields = ['name', 'bio', 'location', 'phone', 'website', 
                         'niche', 'interests', 'business_name', 'business_type',
                         'industry', 'content_needs', 'annual_budget']
        
        for field in allowed_fields:
            if field in data:
                setattr(self, field, data[field])
        
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def sync_instagram_profile(self):
        """Sync Instagram profile data including profile picture."""
        from email_func_app.utils.instagram_api import InstagramAPI
        import os
        from flask import current_app
        import logging
        from datetime import datetime
        
        logger = logging.getLogger(__name__)
        
        try:
            # Get Instagram username from profile URL or stored username
            instagram_username = None
            if self.instagram_profile:
                # Extract username from profile URL or handle
                username_match = re.search(r'instagram\.com/([^/?]+)', self.instagram_profile)
                if username_match:
                    instagram_username = username_match.group(1)
                else:
                    # Remove @ and any trailing slashes
                    instagram_username = self.instagram_profile.strip('@').strip('/')
            
            if not instagram_username:
                logger.error(f"No valid Instagram username found in profile URL: {self.instagram_profile}")
                return False
            
            # Try to get profile info
            logger.info(f"Attempting to fetch Instagram profile for {instagram_username}")
            profile_info = InstagramAPI.get_profile_info_from_username(instagram_username)
            
            if not profile_info:
                logger.error(f"Failed to fetch profile info for {instagram_username}")
                return False
            
            logger.info(f"Successfully fetched profile info for {instagram_username}")
            
            # Handle profile picture
            if profile_info.get('profile_picture_url'):
                logger.info(f"Found profile picture URL: {profile_info['profile_picture_url']}")
                profile_pic_data = InstagramAPI.download_profile_picture(profile_info['profile_picture_url'])
                
                if profile_pic_data:
                    try:
                        # Ensure static folder exists
                        if not os.path.exists(current_app.static_folder):
                            logger.error(f"Static folder does not exist: {current_app.static_folder}")
                            os.makedirs(current_app.static_folder)
                            logger.info(f"Created static folder: {current_app.static_folder}")
                        
                        # Create profile pictures directory if it doesn't exist
                        profile_pics_dir = os.path.join(current_app.static_folder, 'profile_pics')
                        if not os.path.exists(profile_pics_dir):
                            logger.info(f"Creating profile_pics directory: {profile_pics_dir}")
                            os.makedirs(profile_pics_dir)
                        
                        # Generate unique filename
                        filename = f"instagram_{self.id}_{int(datetime.utcnow().timestamp())}.jpg"
                        filepath = os.path.join(profile_pics_dir, filename)
                        
                        # Save the file
                        with open(filepath, 'wb') as f:
                            f.write(profile_pic_data)
                        
                        # Update user's profile image
                        self.profile_image = f"profile_pics/{filename}"
                        logger.info(f"Successfully saved profile picture as {filename}")
                    except Exception as e:
                        logger.error(f"Error saving profile picture: {str(e)}")
                        # Continue with other updates even if profile picture fails
                else:
                    logger.warning("Could not download profile picture")
            else:
                logger.warning("No profile picture URL found in profile info")
            
            try:
                # Update social media account
                instagram_account = self.social_accounts.filter_by(platform='instagram').first()
                
                if instagram_account:
                    instagram_account.username = instagram_username
                    instagram_account.followers = profile_info.get('followers_count')
                    instagram_account.is_verified = profile_info.get('is_verified', False)
                    instagram_account.last_synced = datetime.utcnow()
                    logger.info(f"Updated existing Instagram account for {instagram_username}")
                else:
                    # Create new social media account
                    new_account = SocialMediaAccount(
                        user_id=self.id,
                        platform='instagram',
                        username=instagram_username,
                        profile_url=f"https://instagram.com/{instagram_username}",
                        followers=profile_info.get('followers_count'),
                        is_verified=profile_info.get('is_verified', False),
                        last_synced=datetime.utcnow()
                    )
                    db.session.add(new_account)
                    logger.info(f"Created new Instagram account for {instagram_username}")
                
                # Update user profile if needed
                if profile_info.get('full_name') and not self.name:
                    self.name = profile_info['full_name']
                if profile_info.get('biography') and not self.bio:
                    self.bio = profile_info['biography']
                if profile_info.get('external_url') and not self.website:
                    self.website = profile_info['external_url']
                
                self.updated_at = datetime.utcnow()
                db.session.commit()
                logger.info("Successfully updated Instagram profile data")
                return True
                
            except Exception as e:
                logger.error(f"Error updating Instagram account data: {str(e)}")
                try:
                    db.session.rollback()
                except:
                    pass
                return False
            
        except Exception as e:
            logger.error(f"Error in sync_instagram_profile: {str(e)}")
            try:
                db.session.rollback()
            except:
                pass
            return False

    def __repr__(self):
        return f'<User {self.email}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
