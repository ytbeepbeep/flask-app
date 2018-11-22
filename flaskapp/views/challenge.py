from flask import Blueprint, render_template, request, make_response, flash
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from flaskapp.database import db
from flaskapp.forms import ChallengeForm

challenge = Blueprint('challenge', __name__)

@challenge.route('/challenge',methods=['GET'])
@login_required
def show_challenge():
    # TODO: API call
    challenges = []
    if challenges is None:
        flash('You do not have any challenge', category='error')
    return render_template("challenge.html", challenges=challenges)


@challenge.route('/challenge/<id>',methods=['GET'])
@login_required
def challenge_details(id):

    win_distance = ""
    win_time = ""
    win_avg_speed = ""
    # TODO: API call
    challenge = None
    if challenge is None:
        flash('The challenge does not exist', category='error')
        return make_response(render_template('challenge.html'), 404)
    else:
        # TODO: API call
        run_one = None
        run_two = None
        name_run_one = run_one.name
        name_run_two = run_two.name

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


@challenge.route('/create_challenge', methods=['GET','POST'])
@login_required
def create_form_challenge():
    status=200
    form = ChallengeForm()
    # TODO: API call
    runs = []
    num_runs = runs.count()
    if request.method == 'POST':
            # extract the value of the two forms
            option_first = request.form['run_one']
            option_second = request.form['run_two']
            if int(option_first)<1 or int(option_second)<1 or int(option_first)>num_runs or int(option_second)>num_runs or int(option_first) == int(option_second):
                flash('The run/s do not exist or are the same', category='error')
                status = 400
                return render_template('create_challenge.html', runs=runs, form=form), status
            else:
                if form.validate_on_submit():
                    # TODO: API call
                    return redirect('/challenge') , status
    return render_template('create_challenge.html', runs=runs, form=form) , status