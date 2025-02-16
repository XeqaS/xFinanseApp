from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config
from app.utils.logger import setup_logger

# Inicjalizacja rozszerzeń
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object(Config)
    
    # Inicjalizacja rozszerzeń z aplikacją
    db.init_app(app)
    
    with app.app_context():
        setup_logger(app)
        
        # Import blueprintów
        from app.routes import (
            main_bp,
            accounts_bp,
            transactions_bp,
            expenses_bp,
            calendar_bp
        )
        
        # Rejestracja blueprintów
        app.register_blueprint(main_bp)
        app.register_blueprint(accounts_bp)
        app.register_blueprint(transactions_bp)
        app.register_blueprint(expenses_bp)
        app.register_blueprint(calendar_bp)
        
        # Tworzenie tabel
        db.create_all()
        
        # Inicjalizacja domyślnego konta
        from app.services.account_service import AccountService
        if not AccountService.get_all_accounts():
            AccountService.create_account("Główne konto")
            
    return app