from flask import (render_template, redirect, url_for, flash, abort, request,
                   Blueprint)
from item_catalog import db
from item_catalog.items.forms import ItemForm, DeleteItemForm
from item_catalog.models import Item, User

items = Blueprint('items', __name__)


@items.route('/new_item', methods=['GET', 'POST'])
def new_item():
    """Render a form for creating a new item, or redirect after item
    creation."""
    form = ItemForm()
    user = User.query.first()
    if form.validate_on_submit():
        query = Item.query.filter_by(name=form.name.data,
                                     sport=form.sport.data).first()
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
            return redirect(url_for('main.home'))
    return render_template('new_item.html', form=form, title='New Item')


@items.route('/item/<string:item_name>')
def item(item_name):
    """Render a form for updating an existing item, or redirect after
    item update.

    Keyword arguments:
    item_name -- the name of the item
    """
    item = Item.query.filter_by(name=item_name).first()
    if not item:
        abort(404)
    return render_template('item.html', item=item)


@items.route('/item/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
    """Render a form for updating an existing item, or redirect after
    item update.

    Keyword arguments:
    item_name -- the name of the item
    """
    item = Item.query.filter_by(name=item_name).first()
    if not item:
        abort(404)
    form = ItemForm()
    if form.validate_on_submit():
        if form.name.data != item.name or form.sport.data != item.sport:
            query = Item.query.filter_by(name=form.name.data,
                                         sport=form.sport.data).first()
            if query:
                flash('This sport already has an item with that name.', 'bad')
                return redirect(url_for('items.edit_item',
                                        item_name=item_name))
        else:
            item.name = form.name.data
            item.sport = form.sport.data
            item.category = form.category.data
            item.description = form.description.data
            item.private = form.private.data
            db.session.commit()
            flash(f'"{item.name}" has been updated!', 'good')
            return redirect(url_for('items.item', item_name=item_name))
    elif request.method == 'GET':
        form.name.data = item.name
        form.sport.data = item.sport
        form.category.data = item.category
        form.description.data = item.description
        form.private.data = item.private
    return render_template('edit_item.html', item=item, form=form)


@items.route('/item/<string:item_name>/delete', methods=['GET', 'POST'])
def delete_item(item_name):
    """Render a form for deleting an existing item, or redirect after
    item deletion.

    Keyword arguments:
    item_name -- the name of the item
    """
    item = Item.query.filter_by(name=item_name).first()
    if not item:
        abort(404)
    form = DeleteItemForm()
    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        flash(f'"{item.name}" has been deleted.', 'good')
        return redirect(url_for('main.home'))
    return render_template('delete_item.html', item=item, form=form)
