from flask import Blueprint, render_template, redirect, flash, make_response
from flask_login import current_user, login_user, logout_user, login_required
from flaskapp.database import db, Credential
from flaskapp.forms import LoginForm
from flaskapp.views.home import index

auth = Blueprint('auth', __name__)


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
