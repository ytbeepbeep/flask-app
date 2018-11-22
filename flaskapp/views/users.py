from flask import Blueprint, redirect, render_template, request, flash, make_response, url_for, abort
from flask_login import login_required, current_user, logout_user
from flaskapp.database import db, User, Credential
from flaskapp.auth import admin_required
from flaskapp.forms import UserForm, DeleteForm
from flaskapp.views.home import index


users = Blueprint('users', __name__)


@users.route('/users')
@admin_required  # throws 401 HTTPException
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)

@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
    # A connected user cannot create other users
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated is True:
        return abort(403)

    form = UserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_credential = Credential()
            form.populate_obj(new_credential)
            c = db.session.query(Credential).filter(new_credential.email == Credential.email)
            if c.first() is None:
                # TODO Call API
                new_credential.set_password(form.password.data)  # pw should be hashed with some salt
                db.session.add(new_credential)
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:
                flash('Already existing user', category='error')
                return make_response(render_template('create_user.html', form=form), 409)
        else:
            abort(400)

    return render_template('create_user.html', form=form)


@users.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if not hasattr(current_user, 'is_authenticated') or current_user.is_authenticated is False:
        return make_response(index(), 401)

    form = DeleteForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.authenticate(form.password.data) and hasattr(current_user, 'id'):
                # TODO Call API
                # runs = db.session.query(Run).filter(Run.runner_id == current_user.id)
                # objectives = db.session.query(Objective).filter(Objective.runner_id == current_user.id)
                # reports = db.session.query(Report).filter(Report.runner_id == current_user.id)

                # for run in runs.all():
                #     db.session.delete(run)

                # for report in reports.all():
                #     db.session.delete(report)

                # for objective in objectives.all():
                #     db.session.delete(objective)

                db.session.delete(current_user)
                db.session.commit()
                
                logout_user()  # This will also clean up the remember me cookie if it exists.
                return redirect('/')
            else:
                flash("Incorrect password", category='error')
                return make_response(render_template("delete_user.html", form=form), 401)
        else:
            abort(400)
    return render_template("delete_user.html", form=form)