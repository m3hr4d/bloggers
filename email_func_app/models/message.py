from datetime import datetime
from email_func_app.extensions import db

class Message(db.Model):
    """Message model for storing user messages."""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200))
    body = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, resolved, closed
    parent_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)
    
    # Relationships
    sender_user = db.relationship('User', foreign_keys=[sender_id])
    recipient_user = db.relationship('User', foreign_keys=[recipient_id])
    replies = db.relationship('Message', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def __repr__(self):
        return f'<Message {self.id}: {self.subject}>'

    def get_thread(self):
        """Get all messages in the thread."""
        if self.parent_id:
            return self.parent.get_thread()
        return [self] + [reply for reply in self.replies.all()]

    @property
    def is_ticket(self):
        """Check if this is a support ticket (no parent message)."""
        return self.parent_id is None

    @property
    def thread_status(self):
        """Get the status of the entire thread."""
        if self.parent_id:
            return self.parent.thread_status
        return self.status
