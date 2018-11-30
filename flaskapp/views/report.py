from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from flaskapp.database import Report
from flaskapp.forms import MailForm


import requests
import os

report = Blueprint('report', __name__)

DATA_SERVICE_URL = os.environ['DATA_SERVICE']
MAIL_SERVICE_URL = os.environ['MAIL_SERVICE']


# In this we specify the setting for the management of the report
@report.route('/frequency', methods=['GET', 'POST'])
@login_required
def settingreport():
    status = 200
    form = MailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            choice = request.form['setting_mail']

            freq = (float(choice) * 3600.0)
            reply = requests.post(url="%s/frequency/%s" % (MAIL_SERVICE_URL, current_user.dataservice_user_id), json={'frequency': freq})
            if reply.status_code is 200:
                flash('Settings updated', category='success')
            else:
                flash('An error occurred while setting frequency', category='error')
                status = 500
    return render_template('mail.html', form=form), status

