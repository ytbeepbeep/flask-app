import functools
from flask_login import current_user, LoginManager, fresh_login_required
from flaskapp.database import Credential
from stravalib import Client
import os

login_manager = LoginManager()


def _strava_auth_url():
    client = Client()
    client_id = os.environ['STRAVA_CLIENT_ID']
    redirect = 'http://127.0.0.1:5001/strava_auth'
    url = client.authorization_url(client_id=client_id,
                                   redirect_uri=redirect)
    return url


def strava_auth_url(config):
    return _strava_auth_url()


def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required


@login_manager.user_loader
def load_user(user_id):
    credential = Credential.query.get(user_id)
    if credential is not None:
        credential._authenticated = True
    return credential
