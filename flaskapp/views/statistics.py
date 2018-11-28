from flask import Blueprint, render_template, json, flash
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
    runs = []
    stats = dict()
    try:
        reply = DataService().get("/runs", params={'user_id': current_user.dataservice_user_id})
        runs = reply.json()

        for run in runs:
            print(run)
            stats[run['id']] = [run['average_speed'], run['distance'], run['elapsed_time']]

    except Exception as ex:
        print(ex)
        flash('Cannot get runs data', category='error')

    return render_template("statistics.html", runs=runs, stats=json.dumps(stats))

