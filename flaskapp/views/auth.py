from flask import Blueprint, render_template, redirect, flash, make_response, request
from flask_login import current_user, login_user, logout_user, login_required
from flaskapp.database import db, Credential
from flaskapp.forms import LoginForm
from flaskapp.views.home import index, home
from stravalib import Client
from flaskapp.auth import strava_auth_url
from flaskapp.services import DataService

import os
import requests


auth = Blueprint('auth', __name__)

DATASERVICE = os.environ['DATA_SERVICE']


@auth.route('/strava_auth')
@login_required
def _strava_auth():  # pragma: no cover
    code = request.args.get('code')
    client = Client()
    xc = client.exchange_code_for_token
    access_token = xc(client_id=os.environ['STRAVA_CLIENT_ID'],
                      client_secret=os.environ['STRAVA_CLIENT_SECRET'],
                      code=code)
    user_id = db.session.query(Credential).filter(current_user.id == Credential.id).first().dataservice_user_id

    if user_id is None:
        return make_response(render_template('strava_error.html', auth_url=strava_auth_url()), 409)

    # print('uise: ', access_token)

    if 'access_token' in access_token: # compatibility with stravalib 10
        access_token = access_token['access_token']

    reply = DataService().post('/users/%s'%str(user_id), data={'strava_token': access_token})

    if reply.status_code == 409:
        return make_response(render_template('strava_error.html', auth_url=strava_auth_url()), 409)

    current_user.authorized_strava = True
    db.session.merge(current_user)
    db.session.commit()

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
            return redirect('/')
        else:
            flash('Wrong email or password', category='error')
            return make_response(render_template('login.html', form=form), 401)
    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')
