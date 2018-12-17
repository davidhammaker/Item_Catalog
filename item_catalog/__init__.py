import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = os.environ.get('IC_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('IC_DATABASE')

db = SQLAlchemy(app)

from item_catalog import views
