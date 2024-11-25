from email_func_app import db

class Offer(db.Model):
    """Offer model for storing business offers."""
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_offered = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20))

    def __init__(self, plan_id, business_id, service_offered, description=None):
        self.plan_id = plan_id
        self.business_id = business_id
        self.service_offered = service_offered
        self.description = description
        self.status = 'pending'

    def __repr__(self):
        return f'<Offer {self.id} for Plan {self.plan_id}>'
