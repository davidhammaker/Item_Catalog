from flask import render_template, redirect, url_for, flash, abort, request
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
    user = User.query.first()
    if form.validate_on_submit():
        query = Item.query.filter_by(name=form.name.data, sport=form.sport.data).first()
        if query:
            flash('This sport already has an item with that name.', 'bad')
        else:
            name = form.name.data
            sport = form.sport.data
            category = form.category.data
            description = form.description.data
            private = form.private.data
            item = Item(name=name, sport=sport, category=category,
                        description=description, private=private,
                        user_id=user.id)
            db.session.add(item)
            db.session.commit()
            flash(f'"{name}" has been added!', 'good')
            return redirect(url_for('home'))
    return render_template('new_item.html', form=form, title='New Item')


@app.route('/item/<string:item_name>')
def item(item_name):
    item = Item.query.filter_by(name=item_name).first()
    if not item:
        abort(404)
    return render_template('item.html', item=item)


@app.route('/item/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
    item = Item.query.filter_by(name=item_name).first()
    if not item:
        abort(404)
    form = NewItemForm()
    if form.validate_on_submit():
        if form.name.data != item.name or form.sport.data != item.sport:
            query = Item.query.filter_by(name=form.name.data, sport=form.sport.data).first()
            if query:
                flash('This sport already has an item with that name.', 'bad')
                return redirect(url_for('edit_item', item_name=item_name))
        else:
            item.name = form.name.data
            item.sport = form.sport.data
            item.category = form.category.data
            item.description = form.description.data
            item.private = form.private.data
            db.session.commit()
            flash(f'"{item.name}" has been updated!', 'good')
            return redirect(url_for('item', item_name=item_name))
    elif request.method == 'GET':
        form.name.data = item.name
        form.sport.data = item.sport
        form.category.data = item.category
        form.description.data = item.description
        form.private.data = item.private
    return render_template('edit_item.html', item=item, form=form)
