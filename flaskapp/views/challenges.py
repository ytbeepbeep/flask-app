from flask import Blueprint, render_template, request, make_response, flash
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from flaskapp.database import Challenge
from flaskapp.forms import ChallengeForm

import requests
import os

challenge = Blueprint('challenges', __name__)

DATA_SERVICE_URL = os.environ['DATA_SERVICE']
CHAL_SERVICE_URL = os.environ['CHALLENGE_SERVICE']


@challenge.route('/challenges/<id>',methods=['GET'])
@login_required
def challenge_details(id):
    win_distance = ""
    win_time = ""
    win_avg_speed = ""
    challenge = requests.get(url="%s/challenges/%s" % (CHAL_SERVICE_URL, id), params={'user_id': current_user.dataservice_user_id})
    if challenge is None:
        flash('The challenge does not exist', category='error')
        return make_response(render_template('challenge.html'), 404)
    else:
        run_one = requests.get(url="%s/runs/%s" % (CHAL_SERVICE_URL, challenge.run_one), params={'user_id': id})
        run_two = requests.get(url="%s/runs/%s" % (CHAL_SERVICE_URL, challenge.run_two), params={'user_id': id})
        name_run_one = run_one.title
        name_run_two = run_two.title

        if run_one is None or run_two is None:
            flash('The run/s does not exist', category='error')
            return make_response(render_template('challenge.html'), 404)
        else:

            if run_one.distance == run_two.distance:
                win_distance = "The runs are equal for the distance field"
            elif run_one.distance > run_two.distance:
                win_distance = "The first run win for the distance field"
            else:
                win_distance = "The second run win for the distance field"

            if run_one.elapsed_time == run_two.elapsed_time:
                win_time = "The runs are equal for the time"
            elif run_one.elapsed_time < run_two.elapsed_time:
                win_time = "The first run win for the time"
            else:
                win_time = "The second run win for the time"

            if run_one.average_speed > run_two.average_speed:
                win_avg_speed = "The runs are equal for the average speed"
            elif run_one.average_speed > run_two.average_speed:
                win_avg_speed = "The first run win for the average speed"
            else:
                win_avg_speed = "The second run win for the average speed"

    return render_template('comparechallenge.html', run_one=run_one, run_two=run_two, name_run_one=name_run_one , name_run_two=name_run_two, win_avg_speed=win_avg_speed, win_distance=win_distance, win_time=win_time )


@challenge.route('/challenges', methods=['GET', 'POST', 'DELETE'])
@login_required
def page_challenge():
    status=200
    if request.method == 'GET':
        print("SONO QUI")
        challenges = requests.get(url="%s/challenges" % (CHAL_SERVICE_URL), params={'user_id': current_user.dataservice_user_id})
        if challenges is None:
            flash('You do not have any challenge', category='error')
        return render_template("challenge.html", challenges=challenges)
    
    elif request.method == 'POST':
        form = ChallengeForm()
        if form.validate_on_submit():
            runs = requests.get(url="%s/runs" % (DATA_SERVICE_URL), params={'user_id': id})
            
            run_one_id = request.form['run_one']
            run_two_id = request.form['run_two']

            reply_run_1 = requests.get(url="%s/runs/%s" % (DATA_SERVICE_URL, run_one_id))
            reply_run_2 = requests.get(url="%s/runs/%s" % (DATA_SERVICE_URL, run_two_id))

            if reply_run_1.status_code is not 200 :
                flash('The run/s do not exist or are the same', category='error')
                status = reply_run_1.status_code
                return render_template('create_challenge.html', runs=runs, form=form), status

            if reply_run_2.status_code is not 200 :
                flash('The run/s do not exist or are the same', category='error')
                status = reply_run_2.status_code
                return render_template('create_challenge.html', runs=runs, form=form), status
            else:        
                new_challenge = Challenge()
                name_option_1 = reply_run_1.title
                name_option_2 = reply_run_2.title
                form.populate_obj(new_challenge)
                new_challenge.set_challenge_user(current_user.id)
                new_challenge.set_challenge1_run(run_one_id)
                new_challenge.set_challenge1_name(name_option_1)
                new_challenge.set_challenge2_run(run_two_id)
                new_challenge.set_challenge2_name(name_option_2)
                requests.post(url="%s/challenges" % CHAL_SERVICE_URL, json=new_challenge.to_json())
                return redirect('/challenges') , status
        return render_template('create_challenge.html', runs=runs, form=form) , status
