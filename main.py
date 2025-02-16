from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler
import traceback

# Konfiguracja loggera
def setup_logger():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        'logs/finance_app.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Finance application startup')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Dla obsługi flash messages
db = SQLAlchemy(app)

# Modele
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref=db.backref('transactions', lazy=True))

def init_db():
    try:
        if not os.path.exists("instance/finance.db"):
            db.create_all()
            app.logger.info("Database initialized: finance.db created")
            
            # Dodaj przykładowe konto, jeśli baza jest pusta
            if not Account.query.first():
                default_account = Account(name="Główne konto", balance=0.0)
                db.session.add(default_account)
                db.session.commit()
                app.logger.info("Created default account")
    except Exception as e:
        app.logger.error(f"Database initialization error: {str(e)}\n{traceback.format_exc()}")
        raise

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error rendering index: {str(e)}\n{traceback.format_exc()}")
        flash('Wystąpił błąd podczas ładowania strony głównej', 'error')
        return render_template('error.html', error=str(e)), 500

@app.route('/transactions')
def transactions():
    try:
        transactions = Transaction.query.order_by(Transaction.date.desc(), Transaction.id.desc()).all()
        accounts = Account.query.all()
        
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
                app.logger.error(f"Error processing transaction {transaction.id}: {str(e)}")
                continue
        
        return render_template("transactions.html", 
                             transactions=transaction_list,
                             accounts=accounts)
    except Exception as e:
        app.logger.error(f"Error in transactions view: {str(e)}\n{traceback.format_exc()}")
        flash('Wystąpił błąd podczas ładowania transakcji', 'error')
        return render_template('error.html', error=str(e)), 500

@app.route('/add', methods=['POST'])
def add_transaction():
    try:
        date = request.form['date']
        amount = float(request.form['amount'])
        category = request.form['category']
        transaction_type = request.form['transaction_type']
        description = request.form['description']
        account_id = int(request.form['account_id'])
        
        account = Account.query.get(account_id)
        if not account:
            app.logger.error(f"Account {account_id} not found")
            flash('Wybrane konto nie istnieje', 'error')
            return redirect(url_for('transactions'))
        
        transaction = Transaction(
            date=datetime.strptime(date, '%Y-%m-%d'),
            amount=amount,
            category=category,
            transaction_type=transaction_type,
            description=description,
            account=account
        )
        
        if transaction_type == "inflow":
            account.balance += amount
        elif transaction_type == "outflow":
            if account.balance < amount:
                flash('Niewystarczające środki na koncie', 'warning')
                return redirect(url_for('transactions'))
            account.balance -= amount
        
        db.session.add(transaction)
        db.session.commit()
        app.logger.info(f"Added new transaction: {transaction_type} {amount} to account {account_id}")
        flash('Transakcja została dodana pomyślnie', 'success')
        
    except ValueError as e:
        app.logger.error(f"Value error in add_transaction: {str(e)}")
        flash('Nieprawidłowe dane transakcji', 'error')
    except Exception as e:
        app.logger.error(f"Error in add_transaction: {str(e)}\n{traceback.format_exc()}")
        db.session.rollback()
        flash('Wystąpił błąd podczas dodawania transakcji', 'error')
    
    return redirect(url_for('transactions'))

@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        
        if transaction.transaction_type == "inflow":
            transaction.account.balance -= transaction.amount
        elif transaction.transaction_type == "outflow":
            transaction.account.balance += transaction.amount
        
        db.session.delete(transaction)
        db.session.commit()
        app.logger.info(f"Deleted transaction {transaction_id}")
        flash('Transakcja została usunięta', 'success')
        
    except Exception as e:
        app.logger.error(f"Error deleting transaction {transaction_id}: {str(e)}\n{traceback.format_exc()}")
        db.session.rollback()
        flash('Wystąpił błąd podczas usuwania transakcji', 'error')
    
    return redirect(url_for('transactions'))

@app.route('/edit_transaction/<int:transaction_id>', methods=['POST'])
def edit_transaction(transaction_id):
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        old_amount = transaction.amount
        old_type = transaction.transaction_type
        
        transaction.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        transaction.amount = float(request.form['amount'])
        transaction.category = request.form['category']
        transaction.description = request.form['description']
        
        # Aktualizacja salda konta
        account = transaction.account
        if old_type == "inflow":
            account.balance -= old_amount
        elif old_type == "outflow":
            account.balance += old_amount
            
        if transaction.transaction_type == "inflow":
            account.balance += transaction.amount
        elif transaction.transaction_type == "outflow":
            account.balance -= transaction.amount
        
        db.session.commit()
        app.logger.info(f"Updated transaction {transaction_id}")
        return jsonify({"status": "success"})
        
    except Exception as e:
        app.logger.error(f"Error updating transaction {transaction_id}: {str(e)}\n{traceback.format_exc()}")
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)})

@app.route('/accounts')
def accounts():
    try:
        accounts = Account.query.all()
        return render_template("accounts.html", accounts=accounts)
    except Exception as e:
        app.logger.error(f"Error in accounts view: {str(e)}\n{traceback.format_exc()}")
        flash('Wystąpił błąd podczas ładowania listy kont', 'error')
        return render_template('error.html', error=str(e)), 500

@app.route('/add_account', methods=['POST'])
def add_account():
    try:
        name = request.form['name']
        initial_balance = float(request.form.get('initial_balance', 0.0))
        
        if not name:
            flash('Nazwa konta jest wymagana', 'error')
            return redirect(url_for('accounts'))
            
        account = Account(
            name=name,
            balance=initial_balance
        )
        
        db.session.add(account)
        db.session.commit()
        
        app.logger.info(f"Added new account: {name} with initial balance: {initial_balance}")
        flash('Konto zostało utworzone pomyślnie', 'success')
        
    except ValueError as e:
        app.logger.error(f"Value error in add_account: {str(e)}")
        flash('Nieprawidłowa wartość początkowego salda', 'error')
    except Exception as e:
        app.logger.error(f"Error in add_account: {str(e)}\n{traceback.format_exc()}")
        db.session.rollback()
        flash('Wystąpił błąd podczas tworzenia konta', 'error')
    
    return redirect(url_for('accounts'))

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f'Page not found: {request.url}')
    return render_template('error.html', error="Strona nie została znaleziona"), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}\n{traceback.format_exc()}')
    db.session.rollback()
    return render_template('error.html', error="Wystąpił błąd serwera"), 500

if __name__ == '__main__':
    with app.app_context():
        setup_logger()
        init_db()
    app.run(debug=True)