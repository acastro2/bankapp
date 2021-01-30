from datetime import datetime
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, nullable=False)
    account = db.Column(db.String(20), index=True, unique=True, nullable=False)
    cpf = db.Column(db.String(11), index=True, unique=True, nullable=False)

class TransactionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    from_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    to_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)