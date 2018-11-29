from flask import Blueprint, render_template, abort
from flask_login import login_required
import requests
import os

from flaskapp.database import db

run = Blueprint('run', __name__)

DATASERVICE = os.environ['DATA_SERVICE']


@run.route('/run/<id>', methods=['GET'])
@login_required
def get_run(id):
    reply = requests.get(DATASERVICE + "/runs/%s" % id)
    
    if reply.status_code is not 200:
        abort(reply.status_code)
        
    return render_template("run.html", run=reply.json())
