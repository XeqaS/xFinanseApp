from app.routes.main import bp as main_bp
from app.routes.accounts import bp as accounts_bp
from app.routes.transactions import bp as transactions_bp
from app.routes.expenses import bp as expenses_bp
from app.routes.calendar import bp as calendar_bp

__all__ = ['main_bp', 'accounts_bp', 'transactions_bp', 'expenses_bp', 'calendar_bp']