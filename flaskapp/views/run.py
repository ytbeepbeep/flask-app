from flask import Blueprint, render_template, abort, request, jsonify
from flask_login import login_required
import requests
import os

from flaskapp.database import db

run = Blueprint('run', __name__)

DATASERVICE = os.environ['DATA_SERVICE']


@run.route('/run/<id>', methods=['GET'])
@login_required
def get_run(id):
    run = requests.get(DATASERVICE + "/runs", params={'run_id': id})
    
    if run is None:
        abort(404)
        
    return render_template("run.html", run=run)
