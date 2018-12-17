from flask import render_template
from item_catalog import app
from item_catalog.forms import NewItemForm


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/new_item', methods=['GET', 'POST'])
def new_item():
    form = NewItemForm()
    return render_template('new_item.html', form=form, title='New Item')
