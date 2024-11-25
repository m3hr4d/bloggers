"""Offer model."""
from email_func_app.app import db
from .constants import STATUS_UNDER_REVIEW

class Offer(db.Model):
    """Offer model for business offers on influencer plans."""
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_offered = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default=STATUS_UNDER_REVIEW)

    # Relationship with business
    business = db.relationship('User', backref='offers')

    def __repr__(self):
        """String representation of Offer."""
        return f"Offer(Plan: {self.plan_id}, Business: {self.business_id})"
