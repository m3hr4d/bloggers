from email_func_app.extensions import db
from datetime import datetime

class Niche(db.Model):
    """Model for storing brand niches/categories."""
    __tablename__ = 'niches'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))  # Font Awesome or Bootstrap icon name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Niche {self.name}>'


class Service(db.Model):
    """Model for storing influencer services."""
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))  # Font Awesome or Bootstrap icon name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Service {self.name}>'


# Association tables for many-to-many relationships
user_niches = db.Table('user_niches',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('niche_id', db.Integer, db.ForeignKey('niches.id'), primary_key=True)
)

user_services = db.Table('user_services',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)

# Add these relationships to the User model:
# niches = db.relationship('Niche', secondary=user_niches, lazy='dynamic',
#                         backref=db.backref('users', lazy='dynamic'))
# services = db.relationship('Service', secondary=user_services, lazy='dynamic',
#                          backref=db.backref('users', lazy='dynamic'))
