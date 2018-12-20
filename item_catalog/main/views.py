from flask import (render_template, abort, request, Blueprint, flash,
                   redirect, url_for)
from flask_login import login_required, logout_user, current_user
from item_catalog.models import Item

main = Blueprint('main', __name__)


@main.route('/')
def home():
    """Render the home page with recent items."""
    query = Item.query.filter_by(private=False).order_by(Item.date.desc()).all()
    items = []
    for i in range(10):
        items.append(query[i])
    return render_template('home.html', items=items)


@main.route('/all')
def all_items():
    """Render a page with all items alphabetically."""
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        private_items = Item.query.filter_by(private=True, user=current_user)
        public_items = Item.query.filter_by(private=False)
        items_combo = private_items.union(public_items)
        items = items_combo.order_by(Item.name).paginate(page=page,
                                                         per_page=10)
    else:
        items = Item.query.order_by(Item.name).filter_by(private=False)\
            .paginate(page=page, per_page=10)
    return render_template('all.html', items=items)


@main.route('/my_items')
@login_required
def my_items():
    """Render all of a user's items alphabetically."""
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.name).filter_by(user=current_user)\
        .paginate(page=page, per_page=10)
    return render_template('all.html', items=items, header='My Items')


@main.route('/sport/<string:sport>')
def sport(sport):
    """Render a page with all items for a given sport.

    Keyword arguments:
    sport -- the sport by which items are filtered
    """
    sports = ['Baseball',
              'Basketball',
              'Bowling',
              'Boxing',
              'Football',
              'Golf',
              'Hockey',
              'Soccer',
              'Tennis',
              'Other']
    if sport not in sports:
        abort(404)
    page = request.args.get('page', 1, type=int)
    items = Item.query.filter_by(sport=sport).order_by(Item.name)\
        .paginate(page=page, per_page=10)
    return render_template('all.html', items=items, header=sport)


@main.route('/logout')
@login_required
def logout():
    """Log out the user. Based on Flask-Login and Flask-Dance
    documentation."""
    logout_user()
    flash('You have logged out.', 'neutral')
    return redirect(url_for('main.home'))
