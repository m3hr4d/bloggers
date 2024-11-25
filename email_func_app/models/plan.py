from email_func_app.extensions import db
from datetime import datetime

class Plan(db.Model):
    """Plan model for storing influencer plans."""
    __tablename__ = 'plan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    available_times = db.Column(db.String(200))
    content_suggestions = db.Column(db.Text)
    suggested_price = db.Column(db.Float)
    additional_notes = db.Column(db.Text)
    custom_services = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    offers = db.relationship('Offer', backref='plan', lazy='dynamic')
    niches = db.relationship('Niche', secondary='plan_niches', lazy='dynamic',
                         backref=db.backref('plans', lazy='dynamic'))
    services = db.relationship('Service', secondary='plan_services', lazy='dynamic',
                          backref=db.backref('plans', lazy='dynamic'))

    def __init__(self, influencer_id, title, description, location, start_date, end_date):
        self.influencer_id = influencer_id
        self.title = title
        self.description = description
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f'<Plan {self.title} by Influencer {self.influencer_id}>'


# Association tables for many-to-many relationships
plan_niches = db.Table('plan_niches',
    db.Column('plan_id', db.Integer, db.ForeignKey('plan.id'), primary_key=True),
    db.Column('niche_id', db.Integer, db.ForeignKey('niches.id'), primary_key=True)
)

plan_services = db.Table('plan_services',
    db.Column('plan_id', db.Integer, db.ForeignKey('plan.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)
