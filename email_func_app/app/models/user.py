"""User model."""
from email_func_app.app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """User model for both influencers and businesses."""
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'influencer' or 'business'
    name = db.Column(db.String(100))
    instagram_profile = db.Column(db.String(100))
    location = db.Column(db.String(100))
    profile_image = db.Column(db.String(255))  # Store profile image filename
    bio = db.Column(db.Text)  # For both influencer and business descriptions
    
    # Influencer-specific fields
    niche = db.Column(db.String(100))
    followers = db.Column(db.Integer)
    engagement_rate = db.Column(db.Float)
    
    # Business-specific fields
    business_name = db.Column(db.String(100))
    business_website = db.Column(db.String(200))
    business_type = db.Column(db.String(50))  # 'agency', 'ecommerce', 'website', 'retail', 'other'
    industry = db.Column(db.String(50))  # Primary industry
    categories = db.Column(db.String(255))  # Comma-separated list of categories
    experience_level = db.Column(db.String(20))  # 'new', 'occasional', 'regular'
    content_needs = db.Column(db.String(20))  # '0-5', '5-10', '10-20', '20+'
    annual_budget = db.Column(db.String(20))  # Budget range
    onboarding_completed = db.Column(db.Boolean, default=False)  # Track onboarding completion
    interests = db.Column(db.Text)  # Store JSON string of selected interests

    def __repr__(self):
        """String representation of User."""
        return f"User('{self.email}', '{self.user_type}')"
