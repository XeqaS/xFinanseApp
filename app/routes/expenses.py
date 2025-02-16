from flask import Blueprint, render_template, current_app
from app.services.transaction_service import TransactionService

bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@bp.route('/')
def expenses():
    """Wyświetla stronę z wydatkami."""
    try:
        transactions = TransactionService.get_all_transactions()
        # Filtrujemy tylko wydatki
        expenses = [t for t in transactions if t.transaction_type == "outflow"]
        return render_template("expenses.html", expenses=expenses)
    except Exception as e:
        current_app.logger.error(f"Error in expenses view: {str(e)}")
        return render_template('error.html', error=str(e)), 500