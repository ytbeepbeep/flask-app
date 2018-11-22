from flask import Blueprint, render_template
from flask_login import login_required

from flaskapp.database import db
from flaskapp.auth import current_user

statistics = Blueprint('statistics', __name__)


@statistics.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Inside the template we retrieve data from run/statistics
    using javascript"""
    # TODO: API call
    runs = []
    return render_template("statistics.html", runs=runs)

