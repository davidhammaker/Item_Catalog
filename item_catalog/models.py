from datetime import datetime
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from item_catalog import db


class Item(db.Model):
    """Table for storing items.

    Inherits from:
    db.Model -- the class is a Flask-SQLAlchemy model

    Attributes:
    id -- a db.Column designating a unique integer as the item's primary key
    name -- a db.Column designating a string for the item name
    sport -- a db.Column designating a string for the item's associated sport
    category -- a db.Column designating a string for the item's associated
        category
    description -- a db.Column designating a string for the item's description
    date -- a db.Column designating a DateTime object for the time of the
        item's creation
    private -- a db.Column designating a boolean value representing whether the
        item is private
    user_id -- a db.Column designating an integer representing the item's
        creator
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    sport = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    private = db.Column(db.Boolean, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Item('{self.name}', '{self.sport}', '{self.category}', '{self.date}')"


class User(db.Model, UserMixin):
    """Table for storing users.

    Inherits from:
    db.Model -- the class is a Flask-SQLAlchemy model
    UserMixin -- the class must include UserMixin methods

    Attributes:
    id -- a db.Column designating a unique integer as the user's primary key
    username -- a db.Column designating a string for the user's username
    email -- a db.Column designating a string for the user's email address
    name -- a db.Column designating a string for the user's name
    items -- a db.relationship to the Item class creating a back-reference
        called 'user' for the Item class
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256))
    items = db.relationship('Item', backref='user', lazy=True)


class OAuth(db.Model, OAuthConsumerMixin):
    """Table for storing users.

    Inherits from:
    db.Model -- the class is a Flask-SQLAlchemy model
    OAuthConsumerMixin -- the class must include OAuthConsumerMixin methods

    Attributes:
    provider_user_id -- a db.Column designating a unique string that represents
        the associated OAuth provider
    user_id -- a db.Column designating an integer representing the associated
        user's ID
    user -- a db.relationship to the User class creating a back-reference
        called 'user' for the OAuth class
    """
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
