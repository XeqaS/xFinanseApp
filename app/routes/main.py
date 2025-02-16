from flask import Blueprint, render_template, flash, current_app, request
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        current_app.logger.error(f"Error rendering index: {str(e)}")
        flash('Wystąpił błąd podczas ładowania strony głównej', 'error')
        return render_template('error.html', error=str(e)), 500

@bp.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.error(f'Page not found: {request.url}')
    return render_template('error.html', error="Strona nie została znaleziona"), 404

@bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error(f'Server Error: {error}')
    db.session.rollback()
    return render_template('error.html', error="Wystąpił błąd serwera"), 500