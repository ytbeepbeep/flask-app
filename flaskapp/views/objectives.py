from flask import Blueprint, redirect, render_template, request, flash, make_response, url_for, abort
from flask_login import login_required, current_user
from flaskapp.database import db, Credential, Objective
from flaskapp.auth import admin_required, current_user
from flaskapp.forms import ObjectiveForm
from flaskapp.views.home import home
from stravalib import Client
from datetime import datetime

import os
import requests

objectives = Blueprint('objectives', __name__)

DATASERVICE = os.environ['OBJECTIVE_SERVICE']


@objectives.route('/objectives', methods=['GET'])
@login_required
def _objectives():
    reply = requests.get(DATASERVICE + '/objectives?user_id=' + str(current_user.dataservice_user_id))
    if reply.status_code == 200:
        return render_template("objectives.html", objectives=reply.json())
    else:
        return render_template("objectives.html")


@objectives.route('/create_objective', methods=['GET', 'POST'])
@login_required
def create_objective():
    status = 200
    
    form = ObjectiveForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_objective = Objective()
            form.populate_obj(new_objective)
            new_objective.user_id = current_user.dataservice_user_id
            json = new_objective.to_json()

            reply = requests.post(DATASERVICE + '/objectives', json=json)
            return redirect('/objectives'), status
        else:
            # Bad data were sent
            status = 400
            
    return render_template('create_objective.html', form=form), status
