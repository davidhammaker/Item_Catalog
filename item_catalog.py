import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import NewItemForm

app = Flask(__name__)

app.secret_key = os.environ.get('IC_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('IC_DATABASE')

db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/new_item', methods=['GET', 'POST'])
def new_item():
    form = NewItemForm()
    return render_template('new_item.html', form=form, title='New Item')


if __name__ == '__main__':
    app.run(debug=True)
