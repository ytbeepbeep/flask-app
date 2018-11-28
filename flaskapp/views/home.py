from flask import Blueprint, render_template
from flask_login import current_user
from flaskapp.services import DataService
from flaskapp.auth import strava_auth_url
from stravalib import Client

home = Blueprint('home', __name__)


@home.route('/')
def index():
    user = None
    total_average_speed = None
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        try:
            # TODO
            print("Try to get user data", current_user)
            reply = DataService.get("/user/%s"%current_user.user_id, params={})

            # TODO: get the user
            
            total_average_speed = None # TODO: fix it
        except Exception as ex:
            print("ERROR: ", ex)
            # TODO: Add an error message

    return render_template("index.html", current_user=current_user, strava_auth_url=strava_auth_url(),
                           total_average_speed=total_average_speed)
