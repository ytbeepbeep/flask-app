from flask import Blueprint, render_template, abort, request, jsonify
from flask_login import login_required
from services import DataService
import requests

from flaskapp.database import db

run = Blueprint('run', __name__)


@run.route('/run/<id>', methods=['GET'])
@login_required
def get_run(id):
    run = DataService.do_method(method="GET", url="/runs", params={'run_id': id})
    
    if run is None:
        abort(404)
    return render_template("run.html", run=run)
