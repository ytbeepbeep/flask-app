from flask import Blueprint, render_template, json, flash, make_response
from flask_login import login_required

from flaskapp.database import db
from flaskapp.auth import current_user

from flaskapp.services import DataService

statistics = Blueprint('statistics', __name__)


@statistics.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Inside the template we retrieve data from run/statistics
    using javascript"""
    status_code = 200
    runs = []
    stats = dict()
    try:
        reply = DataService().get("/runs", params={'user_id': current_user.dataservice_user_id})

        if reply.status_code is not 200:
            status_code = reply.status_code
            raise "error"

        runs = reply.json()

        for run in runs:
            stats[run['id']] = [run['average_speed'], run['distance'], run['elapsed_time']]

    except Exception:
        flash('Cannot get runs data', category='error')
        status_code = 500

    return make_response(render_template("statistics.html", runs=runs, stats=json.dumps(stats)), status_code)

