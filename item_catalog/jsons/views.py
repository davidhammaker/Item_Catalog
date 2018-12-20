from flask import Blueprint, jsonify
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
    query = Item.query.filter_by(private=False).order_by(Item.date.desc()).all()
    items = []
    for i in range(10):
        items.append(query[i])
    return jsonify(json_prep(items))
