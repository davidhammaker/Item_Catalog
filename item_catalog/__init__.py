from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from item_catalog.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    """Create a new app instance.

    Keyword arguments:
    config_class -- the configuration class for configuring the
        application (default Config).
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from item_catalog.main.views import main
    from item_catalog.items.views import items
    app.register_blueprint(main)
    app.register_blueprint(items)

    return app
