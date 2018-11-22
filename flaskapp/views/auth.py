from flask import Blueprint, render_template, redirect, request, flash, make_response, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_login import LoginManager, fresh_login_required, confirm_login
from stravalib import Client
from flaskapp.database import db, User, Credential
from flaskapp.views.home import index
from flaskapp.forms import LoginForm
from flaskapp.views.home import strava_auth_url, home, index
auth = Blueprint('auth', __name__)


@auth.route('/strava_auth')
@login_required
def _strava_auth():  # pragma: no cover
    code = request.args.get('code')
    client = Client()
    xc = client.exchange_code_for_token
    access_token = xc(client_id=auth.app.config['STRAVA_CLIENT_ID'],
                      client_secret=auth.app.config['STRAVA_CLIENT_SECRET'],
                      code=code)
    # check if access token exists
    users = db.session.query(User).filter(User.strava_token == access_token)
    if users.first() is not None:
        return make_response(render_template('strava_error.html', auth_url=strava_auth_url(home.app.config)), 409)
    current_user.strava_token = access_token
    db.session.add(current_user)
    db.session.commit()

    ## TODO: API call
    
    return redirect('/')

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated is True:
        return make_response(index(), 403)

    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']

        credential = db.session.query(Credential).filter(Credential.email == email).first()

        if credential is not None and credential.authenticate(password):
            login_user(credential)
            # TODO: get to data-service for retrieve User data and fill User table
            return redirect('/')
        else:
            flash('Wrong email or password', category='error')
            return make_response(render_template('login.html', form=form), 401)
    return render_template('login.html', form=form)

@auth.route("/logout")
def logout():
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated is True:
        logout_user()
        return redirect('/')
    else:
        return make_response(index(), 401)


