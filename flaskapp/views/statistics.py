from flask import Blueprint, render_template
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
    try:
        runs = DataService.get("/runs", params={"user_id": current_user.id})
    except Exception as ex:
        print(ex)
        # TODO: Add an error message

    return render_template("statistics.html", runs=runs)

