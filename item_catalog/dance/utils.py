import os
from flask import flash
from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import login_user, current_user
from item_catalog import db, login_manager
from item_catalog.models import OAuth, User

blueprint = make_github_blueprint(
    client_id=os.environ.get('IC_CLIENT_ID'),
    client_secret=os.environ.get('IC_CLIENT_SECRET')
)


@login_manager.user_loader
def load_user(user_id):
    """Set user_loader callback. Based on Flask-Login and Flask-Dance
    documentation."""
    return User.query.get(int(user_id))


blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)


@oauth_authorized.connect_via(blueprint)
def github_logged_in(blueprint, token):
    """Log in users, storing them in the database if they are not
    already stored. Heavily based on Flask-Dance documentation.

    Keyword Arguments:
    blueprint -- the github blueprint containing the client ID and
        client secret.
    token -- the OAuth authentication token.
    """
    if not token:
        flash('Failed to log in with GitHub.', 'bad')
        return False

    response = blueprint.session.get('/user')
    if not response.ok:
        flash('Failed to fetch user info from GitHub.', 'bad')
        return False

    github_info = response.json()
    github_user_id = str(github_info['id'])

    query = OAuth.query.filter_by(provider=blueprint.name,
                                  provider_user_id=github_user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=github_user_id,
                      token=token)

    if oauth.user:
        login_user(oauth.user)
        flash('Successfully signed in with GitHub!', 'good')
    else:
        user = User(username=github_info['login'], email=github_info['email'],
                    name=github_info['name'])
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)
        flash('Successfully signed in with GitHub!', 'good')
    return False


@oauth_error.connect_via(blueprint)
def github_error(blueprint, error, error_description=None, error_uri=None):
    """Display OAuth provider errors. Heavily based on Flask-Dance
    documentation."""
    message = f'Oauth error from {blueprint.name}! error={error} ' \
        f'description={error_description} uri={error_uri}'
    flash(message, 'bad')
