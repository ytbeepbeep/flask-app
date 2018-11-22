from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from flaskapp.forms import MailForm
from flaskapp.database import db

report = Blueprint('report', __name__)


# In this we specify the setting for the management of the report
@report.route('/settingreport', methods=['GET', 'POST'])
@login_required
def settingreport():
    form = MailForm()
    if request.method == 'POST':
            # TODO: API call
            pass
    return render_template('mail.html', form=form)
