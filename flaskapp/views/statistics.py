from flask import Blueprint, render_template, json, flash, make_response
from flask_login import login_required

from flaskapp.database import db
from flaskapp.auth import current_user

import requests
import os


statistics = Blueprint('statistics', __name__)

DATASERVICE = os.environ['DATA_SERVICE']

@statistics.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Inside the template we retrieve data from run/statistics
    using javascript"""
    status_code = 200
    runs = []
    stats = dict()
    try:
        reply = requests.get(DATASERVICE + "/runs", params={'user_id': current_user.dataservice_user_id})

        if reply.status_code is not 200:
            raise "error"

        runs = reply.json()

        for run in runs:
            stats[run['id']] = [run['average_speed'], run['distance'], run['elapsed_time']]

    except Exception:
        flash('Cannot get runs data', category='error')
        status_code = 500

    return make_response(render_template("statistics.html", runs=runs, stats=json.dumps(stats)), status_code)

