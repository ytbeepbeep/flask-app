from flask import Blueprint, redirect, render_template, request, flash, make_response
from flask_login import login_required, current_user
from flaskapp.database import db, User
from flaskapp.auth import admin_required, current_user
from flaskapp.forms import ObjectiveForm
from flaskapp.views.home import home, strava_auth_url
from stravalib import Client

objectives = Blueprint('objectives', __name__)

@objectives.route('/objectives', methods=['GET'])
@login_required
def _objectives():
    # TODO: API call
    objectives = []
    return render_template("objectives.html", objectives=objectives)


@objectives.route('/create_objective', methods=['GET', 'POST'])
@login_required
def create_objective():
    status = 200
    
    form = ObjectiveForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            # TODO: API call
            
            return redirect('/objectives'), status
        else:
            # Bad data were sent
            status = 400
            
    return render_template('create_objective.html', form=form), status

