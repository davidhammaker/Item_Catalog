import os


class Config:
    SECRET_KEY = os.environ.get('IC_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('IC_DATABASE')