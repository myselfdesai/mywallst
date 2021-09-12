from datetime import datetime
from stripeapp import db
from flask_login import LoginManager, UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.email

class StripeCustomer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stripeCustomerId = db.Column(db.String(255), nullable=False)
    stripeSubscriptionId = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<User id %r>' % self.user_id