from app import db
from datetime import datetime

class Transaction(db.Model):
    """Model transakcji finansowej."""
    
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    
    # Klucz obcy do konta
    account_id = db.Column(
        db.Integer,
        db.ForeignKey('accounts.id', ondelete='CASCADE'),
        nullable=False
    )

    def __init__(self, amount, category, transaction_type, description='', account_id=None, date=None):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.description = description
        self.account_id = account_id
        if date:
            self.date = date

    def __repr__(self):
        return f'Transaction(date={self.date}, amount={self.amount}, type={self.transaction_type})'

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'amount': self.amount,
            'category': self.category,
            'transaction_type': self.transaction_type,
            'description': self.description,
            'account_id': self.account_id
        }