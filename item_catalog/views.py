from flask import render_template, redirect, url_for
from item_catalog import app, db
from item_catalog.forms import NewItemForm
from item_catalog.models import Item, User


@app.route('/')
def home():
    items = Item.query.all()
    return render_template('home.html', items=items)


@app.route('/new_item', methods=['GET', 'POST'])
def new_item():
    form = NewItemForm()
    user = User.query.one()
    if form.validate_on_submit():
        name = form.name.data
        sport = form.sport.data
        category = form.category.data
        description = form.description.data
        item = Item(name=name, sport=sport, category=category, description=description, user_id=user.id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new_item.html', form=form, title='New Item')
