from datetime import datetime
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from item_catalog import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    sport = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Item('{self.name}', '{self.sport}', '{self.category}', '{self.date}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256))
    items = db.relationship('Item', backref='user', lazy=True)


class OAuth(db.Model, OAuthConsumerMixin):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
