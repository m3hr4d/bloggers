from datetime import datetime
from email_func_app.extensions import db
from email_func_app.models.message import Message

class Conversation(db.Model):
    """Conversation model for grouping messages between users."""
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    influencer_user = db.relationship('User', foreign_keys=[influencer_id])
    business_user = db.relationship('User', foreign_keys=[business_id])
    messages = db.relationship('Message', secondary='conversation_messages')
    service_tickets = db.relationship('ServiceTicket', backref='conversation', lazy='dynamic')

    def __repr__(self):
        return f'<Conversation {self.id}>'

# Association table for conversation-message relationship
conversation_messages = db.Table('conversation_messages',
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversations.id'), primary_key=True),
    db.Column('message_id', db.Integer, db.ForeignKey('messages.id'), primary_key=True)
)

class ServiceTicket(db.Model):
    """Service ticket model for managing service requests."""
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # e.g., 'flight', 'hotel', 'car_rental'
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, negotiating
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    influencer_user = db.relationship('User', foreign_keys=[influencer_id])
    business_user = db.relationship('User', foreign_keys=[business_id])

    def __repr__(self):
        return f'<ServiceTicket {self.id}: {self.service_type}>'
