from flask import Blueprint, render_template, request, make_response, flash, abort
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from flaskapp.database import Challenge
from flaskapp.forms import ChallengeForm

import requests
import os

challenges = Blueprint('challenges', __name__)

DATA_SERVICE_URL = os.environ['DATA_SERVICE']
CHAL_SERVICE_URL = os.environ['CHALLENGE_SERVICE']


@challenges.route('/challenges/<id>', methods=['GET'])
@login_required
def challenge_details(id):
    win_distance = ""
    win_time = ""
    win_avg_speed = ""
    challenge_reply = requests.get(url="%s/challenges/%s" % (CHAL_SERVICE_URL, id), params={'user_id': current_user.dataservice_user_id})

    if challenge_reply.status_code is 404:
        abort(404)
    elif challenge_reply.status_code is not 200:
        abort(500)

    challenge = challenge_reply.json()

    run_one_reply = requests.get(url="%s/runs/%s" % (DATA_SERVICE_URL, challenge["run_one"]), params={'user_id': current_user.dataservice_user_id})
    run_two_reply = requests.get(url="%s/runs/%s" % (DATA_SERVICE_URL, challenge["run_two"]), params={'user_id': current_user.dataservice_user_id})

    if run_one_reply.status_code is not 200:
        abort(503)
    if run_two_reply.status_code is not 200:
        abort(500)

    run_one = run_one_reply.json()
    run_two = run_two_reply.json()

    if run_one["distance"] == run_two["distance"]:
        win_distance = "The runs are equal for the distance field"
    elif run_one["distance"] > run_two["distance"]:
        win_distance = "The first run win for the distance field"
    else:
        win_distance = "The second run win for the distance field"

    if run_one["elapsed_time"] == run_two["elapsed_time"]:
        win_time = "The runs are equal for the time"
    elif run_one["elapsed_time"] < run_two["elapsed_time"]:
        win_time = "The first run win for the time"
    else:
        win_time = "The second run win for the time"

    if run_one["average_speed"] > run_two["average_speed"]:
        win_avg_speed = "The runs are equal for the average speed"
    elif run_one["average_speed"] > run_two["average_speed"]:
        win_avg_speed = "The first run win for the average speed"
    else:
        win_avg_speed = "The second run win for the average speed"

    return render_template('comparechallenge.html', run_one=run_one, run_two=run_two, win_avg_speed=win_avg_speed, win_distance=win_distance, win_time=win_time)


@challenges.route('/create_challenge', methods=['GET', 'POST', 'DELETE'])
@login_required
def create_challenge():
    status = 200
    form = ChallengeForm()
    
    runs_reply = requests.get("%s/runs" % (DATA_SERVICE_URL), params={'user_id': current_user.dataservice_user_id})

    if runs_reply.status_code is not 200:
        abort(504)

    runs = runs_reply.json()
    
    if request.method == 'POST':
        if form.validate_on_submit(): 
            
            run_one_id = request.form['run_one']
            run_two_id = request.form['run_two']

            reply_run_1 = requests.get(url="%s/runs/%s" % (DATA_SERVICE_URL, run_one_id))
            reply_run_2 = requests.get(url="%s/runs/%s" % (DATA_SERVICE_URL, run_two_id))

            if reply_run_1.status_code is not 200:
                flash('The run/s do not exist or are the same', category='error')
                status = reply_run_1.status_code
                return render_template('create_challenge.html', runs=runs, form=form), status

            if reply_run_2.status_code is not 200:
                flash('The run/s do not exist or are the same', category='error')
                status = reply_run_2.status_code
                return render_template('create_challenge.html', runs=runs, form=form), status
            else:
                run_1 = reply_run_1.json()
                run_2 = reply_run_2.json()

                new_challenge = Challenge()
                name_option_1 = run_1["title"]
                name_option_2 = run_2["title"]
                form.populate_obj(new_challenge)
                new_challenge.set_challenge_user(current_user.dataservice_user_id)
                new_challenge.set_challenge1_run(run_one_id)
                new_challenge.set_challenge1_name(name_option_1)
                new_challenge.set_challenge2_run(run_two_id)
                new_challenge.set_challenge2_name(name_option_2)
                requests.post(url="%s/challenges" % CHAL_SERVICE_URL, json=new_challenge.to_json())
                return redirect('/challenges') , status

    return render_template('create_challenge.html', runs=runs, form=form), status


@challenges.route('/challenges', methods=['GET'])
@login_required
def page_challenge():
    status = 200
    challenges = None

    reply = requests.get(url="%s/challenges" % (CHAL_SERVICE_URL), params={'user_id': current_user.dataservice_user_id})

    if reply.status_code is 404:
        flash('You do not have any challenge', category='error')
        status = 404
    elif reply.status_code is not 200:
        flash('Server error', category='error')
        status = 500
    else:
        challenges = reply.json()
    
    return render_template("challenge.html", current_user=current_user, challenges=challenges), status
        
