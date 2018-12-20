from flask import Blueprint, render_template

# Create 'errors' blueprint

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """Return a 404 NOT FOUND template."""
    return render_template('errors/404.html')


@errors.app_errorhandler(403)
def error_403(error):
    """Return a 403 FORBIDDEN template."""
    return render_template('errors/403.html')


@errors.app_errorhandler(500)
def error_500(error):
    """Return a 500 SERVER ERROR template."""
    return render_template('errors/500.html')
