from flask import Blueprint, render_template, current_app
from app.services.transaction_service import TransactionService
from datetime import datetime
from collections import defaultdict

bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@bp.route('/')
def calendar():
    """Wyświetla widok kalendarza z transakcjami."""
    try:
        transactions = TransactionService.get_all_transactions()
        
        # Grupowanie transakcji po datach
        transactions_by_date = defaultdict(list)
        for transaction in transactions:
            date_key = transaction.date.strftime('%Y-%m-%d')
            transactions_by_date[date_key].append(transaction)
        
        return render_template(
            "calendar.html",
            transactions_by_date=dict(transactions_by_date),
            current_month=datetime.now().strftime('%Y-%m')
        )
    except Exception as e:
        current_app.logger.error(f"Error in calendar view: {str(e)}")
        return render_template('error.html', error=str(e)), 500