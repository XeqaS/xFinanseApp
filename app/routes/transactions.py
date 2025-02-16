from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, current_app
from app.services.transaction_service import TransactionService
from app.services.account_service import AccountService

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/')
def transactions():
    try:
        transactions = TransactionService.get_all_transactions()
        accounts = AccountService.get_all_accounts()
        
        transaction_list = []
        account_balances = {account.id: account.balance for account in accounts}
        
        for transaction in transactions:
            try:
                transaction_data = {
                    "id": transaction.id,
                    "date": transaction.date.strftime('%Y-%m-%d'),
                    "amount": "{:.2f}".format(transaction.amount),
                    "category": transaction.category,
                    "transaction_type": transaction.transaction_type,
                    "description": transaction.description,
                    "account_name": transaction.account.name,
                    "account_id": transaction.account_id,
                    "balance": "{:.2f}".format(account_balances[transaction.account_id])
                }
                transaction_list.append(transaction_data)
            except Exception as e:
                current_app.logger.error(f"Error processing transaction {transaction.id}: {str(e)}")
                continue
        
        return render_template("transactions.html", 
                             transactions=transaction_list,
                             accounts=accounts)
    except Exception as e:
        current_app.logger.error(f"Error in transactions view: {str(e)}")
        flash('Wystąpił błąd podczas ładowania transakcji', 'error')
        return render_template('error.html', error=str(e)), 500

@bp.route('/add', methods=['POST'])
def add_transaction():
    try:
        date = request.form['date']
        amount = float(request.form['amount'])
        category = request.form['category']
        transaction_type = request.form['transaction_type']
        description = request.form['description']
        account_id = int(request.form['account_id'])
        
        TransactionService.create_transaction(
            date=date,
            amount=amount,
            category=category,
            transaction_type=transaction_type,
            description=description,
            account_id=account_id
        )
        
        current_app.logger.info(f"Added new transaction: {transaction_type} {amount} to account {account_id}")
        flash('Transakcja została dodana pomyślnie', 'success')
        
    except ValueError as e:
        current_app.logger.error(f"Value error in add_transaction: {str(e)}")
        flash(str(e), 'error')
    except Exception as e:
        current_app.logger.error(f"Error in add_transaction: {str(e)}")
        flash('Wystąpił błąd podczas dodawania transakcji', 'error')
    
    return redirect(url_for('transactions.transactions'))

@bp.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    try:
        TransactionService.delete_transaction(transaction_id)
        current_app.logger.info(f"Deleted transaction {transaction_id}")
        flash('Transakcja została usunięta', 'success')
        
    except Exception as e:
        current_app.logger.error(f"Error deleting transaction {transaction_id}: {str(e)}")
        flash('Wystąpił błąd podczas usuwania transakcji', 'error')
    
    return redirect(url_for('transactions.transactions'))

@bp.route('/edit/<int:transaction_id>', methods=['POST'])
def edit_transaction(transaction_id):
    try:
        transaction = TransactionService.update_transaction(
            transaction_id=transaction_id,
            date=request.form['date'],
            amount=float(request.form['amount']),
            category=request.form['category'],
            description=request.form['description']
        )
        
        current_app.logger.info(f"Updated transaction {transaction_id}")
        return jsonify({"status": "success"})
        
    except Exception as e:
        current_app.logger.error(f"Error updating transaction {transaction_id}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})