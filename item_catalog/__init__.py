from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from item_catalog.config import Config

# Create SQLAlchemy instance
db = SQLAlchemy()

# Create and configure LoginManager instance
login_manager = LoginManager()
login_manager.login_view = 'github.login'
login_manager.login_message_category = 'neutral'


def create_app(config_class=Config):
    """Create a new app instance.

    Keyword arguments:
    config_class -- the configuration class for configuring the
        application (default Config).
    """

    # Create and configure Flask instance
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy and LoginManager instances
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from item_catalog.main.views import main
    from item_catalog.items.views import items
    from item_catalog.dance.utils import blueprint as dance
    from item_catalog.jsons.views import jsons
    app.register_blueprint(main)
    app.register_blueprint(items)
    app.register_blueprint(dance, url_prefix='/login')
    app.register_blueprint(jsons)

    return app
