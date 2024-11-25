"""Plan model."""
from email_func_app.app import db
from .constants import STATUS_PENDING, STATUS_ACCEPTED

class Plan(db.Model):
    """Plan model for influencer travel plans."""
    
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
        """Check if plan can be edited."""
        return (
            self.status != STATUS_ACCEPTED and  # Not accepted
            self.edit_count < 1 and            # Not edited before
            len(self.offers) == 0              # No offers received
        )

    def can_delete(self):
        """Check if plan can be deleted."""
        return (
            self.status != STATUS_ACCEPTED and  # Not accepted
            len(self.offers) == 0              # No offers received
        )

    def __repr__(self):
        """String representation of Plan."""
        return f"Plan('{self.destination}', '{self.start_date}' to '{self.end_date}')"
