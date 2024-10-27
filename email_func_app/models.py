from email_func_app import db
from flask_login import UserMixin

STATUS_PENDING = "در حال انتظار"
STATUS_APPROVED = "تایید شده"
STATUS_REJECTED = "رد شده"
STATUS_UNDER_REVIEW = "در انتظار بررسی"
STATUS_ACCEPTED = "پذیرفته شده"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'influencer' or 'business'
    name = db.Column(db.String(100))
    instagram_profile = db.Column(db.String(100))
    location = db.Column(db.String(100))
    
    # Influencer-specific fields
    niche = db.Column(db.String(100))
    followers = db.Column(db.Integer)
    engagement_rate = db.Column(db.Float)
    
    # Business-specific fields
    business_name = db.Column(db.String(100))
    business_website = db.Column(db.String(200))

    def __repr__(self):
        return f"User('{self.email}', '{self.user_type}')"

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(10), nullable=False)  # Store as string for Persian date
    end_date = db.Column(db.String(10), nullable=False)    # Store as string for Persian date
    time = db.Column(db.String(50))
    services_requested = db.Column(db.Text)
    topics_of_interest = db.Column(db.Text)
    status = db.Column(db.String(20), default=STATUS_PENDING)
    edit_count = db.Column(db.Integer, default=0)  # Track number of edits

    # Relationships
    influencer = db.relationship('User', backref='plans')
    offers = db.relationship('Offer', backref='plan', lazy=True)

    def can_edit(self):
        """Check if plan can be edited"""
        return (
            self.status != STATUS_ACCEPTED and  # Not accepted
            self.edit_count < 1 and            # Not edited before
            len(self.offers) == 0              # No offers received
        )

    def can_delete(self):
        """Check if plan can be deleted"""
        return (
            self.status != STATUS_ACCEPTED and  # Not accepted
            len(self.offers) == 0              # No offers received
        )

    def __repr__(self):
        return f"Plan('{self.destination}', '{self.start_date}' to '{self.end_date}')"

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_offered = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default=STATUS_UNDER_REVIEW)

    # Relationship with business
    business = db.relationship('User', backref='offers')

    def __repr__(self):
        return f"Offer(Plan: {self.plan_id}, Business: {self.business_id})"
