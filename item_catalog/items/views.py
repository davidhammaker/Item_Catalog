from flask import (render_template, redirect, url_for, flash, abort, request,
                   Blueprint)
from flask_login import login_required, current_user
from item_catalog import db
from item_catalog.items.forms import ItemForm, DeleteItemForm
from item_catalog.models import Item

# Create 'items' blueprint
items = Blueprint('items', __name__)


@items.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    """Render a form for creating a new item, or redirect after item
    creation."""
    form = ItemForm()
    user = current_user

    # If the form is validated, add its data to the database
    if form.validate_on_submit():

        # Check that an item with the same name and sport does not
        # already exist, or send a flash message and do not add the
        # new item to the database
        query = Item.query.filter_by(name=form.name.data,
                                     sport=form.sport.data).first()
        if query:
            flash('This sport already has an item with that name.', 'bad')

        # If the item does not yet exist, add all details to the
        # database, send a flash message, and redirect to 'home'
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
    """Render a page with information for a specific item.

    Keyword arguments:
    item_name -- the name of the item
    """
    item = Item.query.filter_by(name=item_name).first()

    # If the URL contains a bad item name, send a 404
    if not item:
        abort(404)

    # If the current user is not authorized to view the item because
    # the item is private and was created by a different user, send a
    # 403
    elif item.private and current_user != item.user:
        abort(403)

    return render_template('item.html', item=item)


@items.route('/item/<string:item_name>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_name):
    """Render a form for updating an existing item, or redirect after
    item update.

    Keyword arguments:
    item_name -- the name of the item
    """
    item = Item.query.filter_by(name=item_name).first()

    # If the URL contains a bad item name, send a 404
    if not item:
        abort(404)

    # If the current user is not authorized to edit the item because
    # the item was created by a different user, send a 403
    elif current_user != item.user:
        abort(403)

    form = ItemForm()

    # If the form is validated, update the item with its data to the
    # database
    if form.validate_on_submit():

        # If the item name or sport has been modified, check that an
        # item with the same name and sport does not already exist, or
        # send a flash message and do not add the new item to the
        # database
        if form.name.data != item.name or form.sport.data != item.sport:
            query = Item.query.filter_by(name=form.name.data,
                                         sport=form.sport.data).first()
            if query:
                flash('This sport already has an item with that name.', 'bad')
                return redirect(url_for('items.edit_item',
                                        item_name=item_name))

        # If the item name or sport has not been modified, update all
        # details to the database, send a flash message, and redirect
        # to 'home'
        else:
            item.name = form.name.data
            item.sport = form.sport.data
            item.category = form.category.data
            item.description = form.description.data
            item.private = form.private.data
            db.session.commit()
            flash(f'"{item.name}" has been updated!', 'good')
            return redirect(url_for('items.item', item_name=item_name))

    # If the form is being requested, not submitted, pre-fill the form
    # with existing item data
    elif request.method == 'GET':
        form.name.data = item.name
        form.sport.data = item.sport
        form.category.data = item.category
        form.description.data = item.description
        form.private.data = item.private

    return render_template('edit_item.html', item=item, form=form)


@items.route('/item/<string:item_name>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(item_name):
    """Render a form for deleting an existing item, or redirect after
    item deletion.

    Keyword arguments:
    item_name -- the name of the item
    """
    item = Item.query.filter_by(name=item_name).first()

    # If the URL contains a bad item name, send a 404
    if not item:
        abort(404)

    # If the current user is not authorized to delete the item because
    # the item was created by a different user, send a 403
    elif current_user != item.user:
        abort(403)

    form = DeleteItemForm()

    # If the form is submitted, delete the item from the database,
    # send a flash message, and redirect home
    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        flash(f'"{item.name}" has been deleted.', 'good')
        return redirect(url_for('main.home'))

    return render_template('delete_item.html', item=item, form=form)
