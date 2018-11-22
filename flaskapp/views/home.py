from flask import Blueprint, render_template, request, flash
from stravalib import Client
from flask_login import current_user, LoginManager, login_required, confirm_login
from flaskapp.database import db
from flaskapp.forms import MailForm
from datetime import time

home = Blueprint('home', __name__)


def _strava_auth_url(config):
    client = Client()
    client_id = config['STRAVA_CLIENT_ID']
    redirect = 'http://127.0.0.1:5000/strava_auth'
    url = client.authorization_url(client_id=client_id,
                                   redirect_uri=redirect)
    return url


def strava_auth_url(config):
    return _strava_auth_url(config)

@home.route('/')
def index():
    print("user: ", current_user)
    print("is auth?: ", hasattr(current_user, 'is_authenticated'))
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # TODO: API call
        total_average_speed = 123
        runs = None
    else:
        runs = None
        total_average_speed = 0
    strava_auth_url_ = strava_auth_url(home.app.config)
    return render_template("index.html", runs=runs,
                           strava_auth_url=strava_auth_url_, total_average_speed=total_average_speed)
