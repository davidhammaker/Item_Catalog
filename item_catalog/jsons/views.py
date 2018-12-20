from flask import Blueprint, jsonify, abort
from item_catalog.models import Item
from item_catalog.jsons.utils import json_prep

jsons = Blueprint('jsons', __name__)


@jsons.route('/all/JSON')
def all_items_json():
    """Render a JSON page with all public items."""
    items = Item.query.order_by(Item.name).filter_by(private=False).all()
    return jsonify(json_prep(items))


@jsons.route('/recent/JSON')
def recent_json():
    """Render a JSON page with recent items."""
    query = Item.query.filter_by(private=False).order_by(Item.date.desc())\
        .all()
    items = []
    for i in range(10):
        items.append(query[i])
    return jsonify(json_prep(items))


@jsons.route('/sport/<string:sport>/JSON')
def sport_json(sport):
    """Render a JSON page with all public items for a given sport.

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
    items = Item.query.filter_by(sport=sport, private=False)\
        .order_by(Item.name).all()
    return jsonify(json_prep(items))


@jsons.route('/category/<string:category>/JSON')
def category_json(category):
    """Render a JSON page with all public items for a given category.

    Keyword arguments:
    category -- the category by which items are filtered
    """
    categories = ['Accessories',
                  'Apparel',
                  'Equipment',
                  'Fan Gear']
    if category not in categories:
        abort(404)
    items = Item.query.filter_by(category=category, private=False)\
        .order_by(Item.name).all()
    return jsonify(json_prep(items))
