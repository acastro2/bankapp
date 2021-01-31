from datetime import datetime
from sqlalchemy import CheckConstraint

from app import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, nullable=False)
    account = db.Column(db.String(20), index=True, unique=True, nullable=False)
    cpf = db.Column(db.String(11), index=True, unique=True, nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    from_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    to_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    __table_args__ = (CheckConstraint(
        'NOT(from_customer_id IS NULL AND to_customer_id IS NULL)'),)
