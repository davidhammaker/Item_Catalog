from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from item_catalog.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'github.login'
login_manager.login_message_category = 'neutral'


def create_app(config_class=Config):
    """Create a new app instance.

    Keyword arguments:
    config_class -- the configuration class for configuring the
        application (default Config).
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from item_catalog.main.views import main
    from item_catalog.items.views import items
    from item_catalog.dance.utils import blueprint as dance
    app.register_blueprint(main)
    app.register_blueprint(items)
    app.register_blueprint(dance, url_prefix='/login')

    return app
