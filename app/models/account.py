from app import db
from datetime import datetime

class Account(db.Model):
    """Model konta bankowego."""
    
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Relacja jeden do wielu z transakcjami
    transactions = db.relationship(
        'Transaction',
        backref=db.backref('account', lazy=True),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance

    def __repr__(self):
        return f'Account(name={self.name}, balance={self.balance})'

    def update_balance(self, amount, is_inflow=True):
        if is_inflow:
            self.balance += amount
        else:
            self.balance -= amount
        return self.balance

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'balance': self.balance,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }