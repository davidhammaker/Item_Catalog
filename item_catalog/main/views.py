from flask import render_template, abort, request, Blueprint
from item_catalog.models import Item

main = Blueprint('main', __name__)


@main.route('/')
def home():
    query = Item.query.order_by(Item.date.desc()).all()
    items = []
    for i in range(10):
        items.append(query[i])
    return render_template('home.html', items=items)


@main.route('/all')
def all_items():
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.name).paginate(page=page, per_page=10)
    return render_template('all.html', items=items)


@main.route('/sport/<string:sport>')
def sport(sport):
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
    items = Item.query.filter_by(sport=sport).order_by(Item.name).paginate(page=page, per_page=10)
    return render_template('all.html', items=items)