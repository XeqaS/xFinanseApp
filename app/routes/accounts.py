from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app.services.account_service import AccountService
from app.services.transaction_service import TransactionService

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@bp.route('/')
def accounts():
    """Wyświetla listę wszystkich kont."""
    try:
        accounts = AccountService.get_all_accounts()
        total_balance = sum(account.balance for account in accounts)
        return render_template("accounts.html", accounts=accounts, total_balance=total_balance)
    except Exception as e:
        current_app.logger.error(f"Error in accounts view: {str(e)}")
        flash('Wystąpił błąd podczas ładowania listy kont', 'error')
        return render_template('error.html', error=str(e)), 500

@bp.route('/add', methods=['POST'])
def add_account():
    """Dodaje nowe konto."""
    try:
        name = request.form['name']
        initial_balance = float(request.form.get('initial_balance', 0.0))
        
        if not name:
            flash('Nazwa konta jest wymagana', 'error')
            return redirect(url_for('accounts.accounts'))
            
        AccountService.create_account(name, initial_balance)
        current_app.logger.info(f"Added new account: {name} with initial balance: {initial_balance}")
        flash('Konto zostało utworzone pomyślnie', 'success')
        
    except ValueError as e:
        current_app.logger.error(f"Value error in add_account: {str(e)}")
        flash('Nieprawidłowa wartość początkowego salda', 'error')
    except Exception as e:
        current_app.logger.error(f"Error in add_account: {str(e)}")
        flash('Wystąpił błąd podczas tworzenia konta', 'error')
    
    return redirect(url_for('accounts.accounts'))

@bp.route('/edit/<int:account_id>', methods=['POST'])
def edit_account(account_id):
    """Edytuje istniejące konto."""
    try:
        name = request.form['name']
        balance = float(request.form['balance'])
        
        if not name:
            return jsonify({
                'status': 'error',
                'message': 'Nazwa konta jest wymagana'
            })
            
        account = AccountService.update_account_with_balance(account_id, name, balance)
        if account:
            current_app.logger.info(f"Updated account {account_id}: {name} with balance: {balance}")
            return jsonify({'status': 'success'})
        else:
            return jsonify({
                'status': 'error',
                'message': 'Konto nie zostało znalezione'
            })
            
    except Exception as e:
        current_app.logger.error(f"Error updating account {account_id}: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@bp.route('/delete/<int:account_id>')
def delete_account(account_id):
    """Usuwa konto i wszystkie powiązane z nim transakcje."""
    try:
        # Najpierw usuń wszystkie transakcje powiązane z kontem
        TransactionService.delete_account_transactions(account_id)
        
        # Następnie usuń samo konto
        if AccountService.delete_account(account_id):
            current_app.logger.info(f"Deleted account {account_id}")
            flash('Konto zostało usunięte pomyślnie', 'success')
        else:
            flash('Konto nie zostało znalezione', 'error')
            
    except Exception as e:
        current_app.logger.error(f"Error deleting account {account_id}: {str(e)}")
        flash('Wystąpił błąd podczas usuwania konta', 'error')
    
    return redirect(url_for('accounts.accounts'))