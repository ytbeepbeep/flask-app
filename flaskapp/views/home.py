from flask import Blueprint, render_template
from flask_login import current_user
from flaskapp.auth import strava_auth_url
from stravalib import Client

import requests
import functools
import os

home = Blueprint('home', __name__)

DATASERVICE = os.environ['DATA_SERVICE']

@home.route('/')
def index():
    user = None
    runs = {}
    total_average_speed = None
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        try:
            print("Try to get user data", current_user)
            reply = requests.get(DATASERVICE + "/users/%s" % current_user.dataservice_user_id)

            user = reply.json()

            reply = requests.get(DATASERVICE + "/runs", params={'user_id': current_user.dataservice_user_id})
            if reply is not None:
                runs = reply.json()
                if len(runs) > 0:
                    total_average_speed = functools.reduce(lambda x, y: x + y, [run['average_speed'] for run in runs], 0) / len(runs)

        except Exception as ex:
            print("ERROR: ", ex)

    return render_template("index.html", credential=current_user, user=user, strava_auth_url=strava_auth_url(),
                           total_average_speed=total_average_speed, runs=runs)
