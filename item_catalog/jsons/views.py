from flask import Blueprint, jsonify, abort, render_template
from item_catalog.models import Item
from item_catalog.jsons.utils import json_prep

# Create 'jsons' blueprint

jsons = Blueprint('jsons', __name__)


@jsons.route('/all/JSON')
def all_items_json():
    """Render a JSON page with all public items, listed alphabetically
    by name."""
    items = Item.query.order_by(Item.name).filter_by(private=False).all()
    return jsonify(json_prep(items))


@jsons.route('/recent/JSON')
def recent_json():
    """Render a JSON page with recent items, listed chronologically
    by date, descending."""

    # Find all items that are not private, ordered by date, descending
    query = Item.query.filter_by(private=False).order_by(Item.date.desc())\
        .all()
    items = []

    # Create a list of the most recent 10 items
    for i in range(10):
        items.append(query[i])

    return jsonify(json_prep(items))


@jsons.route('/sport/<string:sport>/JSON')
def sport_json(sport):
    """Render a JSON page with all public items for a given sport,
    listed alphabetically by name.

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

    items = Item.query.filter_by(sport=sport, private=False)\
        .order_by(Item.name).all()
    return jsonify(json_prep(items))


@jsons.route('/category/<string:category>/JSON')
def category_json(category):
    """Render a JSON page with all public items for a given category,
    listed alphabetically by name.

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

    items = Item.query.filter_by(category=category, private=False)\
        .order_by(Item.name).all()
    return jsonify(json_prep(items))


@jsons.route('/item/<string:item_name>/JSON')
def item_json(item_name):
    """Render a JSON page with information for a specific item.

    Keyword arguments:
    item_name -- the name of the item
    """
    item = Item.query.filter_by(name=item_name, private=False).first()

    # If the URL contains a bad item name, send a 404
    if not item:
        abort(404)

    return jsonify(json_prep(item))


@jsons.route('/other/directory')
def directory():
    """Render a template with a list of JSON endpoints."""
    return render_template('directory.html')
