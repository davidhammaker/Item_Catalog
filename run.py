import sys
from item_catalog import create_app, db

app = create_app()


if __name__ == '__main__':
    if '--setup' in sys.argv:
        with app.app_context():
            db.create_all()
            db.session.commit()
    app.run(debug=True)
