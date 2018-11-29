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
@report.route('/frequency/<user_id>', methods=['GET', 'POST'])
@login_required
def settingreport():
    form = MailForm()
    if request.method == 'GET':
        requests.get(url="%s/frequency" % (MAIL_SERVICE_URL), params={'user_id': current_user.dataservice_user_id})
    if request.method == 'POST':
        freq = request.form['setting_mail']
        # MISS PARSING OF THE FREQUENCY
        # print(freq)
        reply = requests.post(url="%s/frequency/", data={'user_id': current_user.dataservice_user_id, 'frequency': freq})  # wrong here
        if reply.status_code == 200:
            flash('Settings updated', category='success')
    return render_template('mail.html', form=form)
