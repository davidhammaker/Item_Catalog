from flask import (render_template, abort, request, Blueprint, flash,
                   redirect, url_for)
from flask_login import login_required, logout_user, current_user
from item_catalog.models import Item

# Create 'main' blueprint
main = Blueprint('main', __name__)


@main.route('/')
def home():
    """Render the home page with 10 most recent items, listed
    chronologically by date, descending."""

    # Find all items that are not private, ordered by date, descending
    query = Item.query.filter_by(private=False).order_by(Item.date.desc()).all()

    # Create a list of the most recent 10 items
    items = []
    for i in range(10):
        try:
            items.append(query[i])
        except IndexError:
            break

    return render_template('home.html', items=items)


@main.route('/all')
def all_items():
    """Render a page with all items alphabetically."""

    # Set up the current page, which defaults to 1 and is always an
    # integer
    page = request.args.get('page', 1, type=int)

    # If the user is logged in, 'items' is the union of all public
    # items and the user's private items. Items are paginated given
    # the current page, with 10 items per page.
    if current_user.is_authenticated:
        private_items = Item.query.filter_by(private=True, user=current_user)
        public_items = Item.query.filter_by(private=False)
        items_combo = private_items.union(public_items)
        items = items_combo.order_by(Item.name).paginate(page=page,
                                                         per_page=10)

    # If the user is not logged in, 'items' is all public items. Items
    # are paginated given the current page, with 10 items per page.
    else:
        items = Item.query.order_by(Item.name).filter_by(private=False)\
            .paginate(page=page, per_page=10)

    return render_template('all.html', items=items, view='all_items')


@main.route('/my_items')
@login_required
def my_items():
    """Render all of a user's items alphabetically."""

    # Set up the current page, which defaults to 1 and is always an
    # integer
    page = request.args.get('page', 1, type=int)

    # 'items' is all of the user's items. Items are paginated given
    # the current page, with 10 items per page.
    items = Item.query.order_by(Item.name).filter_by(user=current_user)\
        .paginate(page=page, per_page=10)

    return render_template('all.html', items=items, header='My Items', view='my_items')


@main.route('/sport/<string:sport>')
def sport(sport):
    """Render a page with all items for a given sport.

    Keyword arguments:
    sport -- the sport by which items are filtered
    """

    # Set up a list of sports
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

    # If the URL contains a bad sport, send a 404
    if sport not in sports:
        abort(404)

    # Set up the current page, which defaults to 1 and is always an
    # integer
    page = request.args.get('page', 1, type=int)

    # If the user is logged in, 'items' is the union of all public
    # items and the user's private items, filtered by the given sport.
    # Items are paginated given the current page, with 10 items per
    # page.
    if current_user.is_authenticated:
        private_items = Item.query.filter_by(private=True, user=current_user,
                                             sport=sport)
        public_items = Item.query.filter_by(private=False, sport=sport)
        items_combo = private_items.union(public_items)
        items = items_combo.order_by(Item.name).paginate(page=page,
                                                         per_page=10)

    # If the user is not logged in, 'items' is all public items,
    # filtered by the given sport. Items are paginated given the
    # current page, with 10 items per page.
    else:
        items = Item.query.filter_by(sport=sport, private=False)\
            .order_by(Item.name).paginate(page=page, per_page=10)
    return render_template('all.html', items=items, header=sport, view='sport')


@main.route('/category/<string:category>')
def category(category):
    """Render a page with all items for a given category.

    Keyword arguments:
    category -- the category by which items are filtered
    """

    # Set up a list of categories
    categories = ['Accessories',
                  'Apparel',
                  'Equipment',
                  'Fan Gear']

    # If the URL contains a bad category, send a 404
    if category not in categories:
        abort(404)

    # Set up the current page, which defaults to 1 and is always an
    # integer
    page = request.args.get('page', 1, type=int)

    # If the user is logged in, 'items' is the union of all public
    # items and the user's private items, filtered by the given
    # category. Items are paginated given the current page, with 10
    # items per page.
    if current_user.is_authenticated:
        private_items = Item.query.filter_by(private=True, user=current_user,
                                             category=category)
        public_items = Item.query.filter_by(private=False, category=category)
        items_combo = private_items.union(public_items)
        items = items_combo.order_by(Item.name).paginate(page=page,
                                                         per_page=10)

    # If the user is not logged in, 'items' is all public items,
    # filtered by the given category. Items are paginated given the
    # current page, with 10 items per page.
    else:
        items = Item.query.filter_by(category=category, private=False)\
            .order_by(Item.name).paginate(page=page, per_page=10)
    return render_template('all.html', items=items, header=category, view='category')


@main.route('/logout')
@login_required
def logout():
    """Log out the user. Based on Flask-Login and Flask-Dance
    documentation."""
    logout_user()
    flash('You have logged out.', 'neutral')
    return redirect(url_for('main.home'))
