from app import db
from app.models.transaction import Transaction
from app.services.account_service import AccountService
from datetime import datetime

class TransactionService:
    @staticmethod
    def create_transaction(date, amount, category, transaction_type, description, account_id):
        account = AccountService.get_account(account_id)
        if not account:
            raise ValueError("Account not found")

        if transaction_type == "outflow" and account.balance < amount:
            raise ValueError("Insufficient funds")

        transaction = Transaction(
            date=datetime.strptime(date, '%Y-%m-%d') if isinstance(date, str) else date,
            amount=amount,
            category=category,
            transaction_type=transaction_type,
            description=description,
            account_id=account_id
        )

        AccountService.update_balance(
            account_id, 
            amount, 
            is_inflow=(transaction_type == "inflow")
        )

        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def get_all_transactions():
        return Transaction.query.order_by(Transaction.date.desc(), Transaction.id.desc()).all()

    @staticmethod
    def delete_transaction(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            AccountService.update_balance(
                transaction.account_id,
                transaction.amount,
                is_inflow=(transaction.transaction_type == "outflow")
            )
            db.session.delete(transaction)
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_transaction(transaction_id, date, amount, category, description):
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            old_amount = transaction.amount
            old_type = transaction.transaction_type
            
            transaction.date = datetime.strptime(date, '%Y-%m-%d') if isinstance(date, str) else date
            transaction.amount = amount
            transaction.category = category
            transaction.description = description
            
            # Zaktualizuj saldo konta
            account = transaction.account
            if old_type == "inflow":
                account.balance -= old_amount
            elif old_type == "outflow":
                account.balance += old_amount
                
            if transaction.transaction_type == "inflow":
                account.balance += amount
            elif transaction.transaction_type == "outflow":
                account.balance -= amount
            
            db.session.commit()
            return transaction
        return None