import os
from flask import flash
from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import login_user, current_user
from item_catalog import db, login_manager
from item_catalog.models import OAuth, User

# Set up Flask-Dance GitHub blueprint
blueprint = make_github_blueprint(
    client_id=os.environ.get('IC_CLIENT_ID'),
    client_secret=os.environ.get('IC_CLIENT_SECRET')
)


@login_manager.user_loader
def load_user(user_id):
    """Set user_loader callback. Based on Flask-Login and Flask-Dance
    documentation."""
    return User.query.get(int(user_id))


# Set up SQLAlchemy backend
blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)


@oauth_authorized.connect_via(blueprint)
def github_logged_in(blueprint, token):
    """Log in users, storing them in the database if they are not
    already stored. Heavily based on Flask-Dance documentation. Return
    False to ensure that Flask-Dance does not save the OAuth token by
    default.

    Keyword Arguments:
    blueprint -- the github blueprint containing the client ID and
        client secret.
    token -- the OAuth authentication token.
    """

    # If no token is given, send a flash message and return
    if not token:
        flash('Failed to log in with GitHub.', 'bad')
        return False

    # Retrieve user information
    response = blueprint.session.get('/user')

    # If user information cannot be retrieved, send a flash message
    # and return
    if not response.ok:
        flash('Failed to fetch user info from GitHub.', 'bad')
        return False

    github_info = response.json()
    github_user_id = str(github_info['id'])

    # Search for the user's GitHub ID in the database
    query = OAuth.query.filter_by(provider=blueprint.name,
                                  provider_user_id=github_user_id)
    try:
        oauth = query.one()

    # If the user's GitHub ID cannot be found in the database, add the
    # user's GitHub ID and OAuth token to the database
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=github_user_id,
                      token=token)

    # If the user is already in the database, log in the user and send
    # a flash message
    if oauth.user:
        login_user(oauth.user)
        flash('Successfully signed in with GitHub!', 'good')

    # If the user is not already in the database associate the user
    # with the corresponding GitHub ID and OAuth token, then add the
    # user and GitHub/OAuth information to the database
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
