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


    """
swagger: "2.0"
info:
  title: BeepBeep Mail Service
  description: Manage email preferences
  license:
    name: AGPL-3.0
    url: https://www.gnu.org/licenses/agpl-3.0.en.html
  version: 0.2.0
basePath: /api
paths:
    /frequency/{user_id}:
      get:
        operationId: getFrequency
        description: Get the frequency preference for mail
        produces:
          - application/json
        parameters:
          - name: user_id
            in: path
            description: ID of user
            required: true
            type: integer
        responses:
          '200':
            description: The current value of the frequency in hour (float)
          '404':
            description: user_id not found, there is not frequency set
      post:
        operationId: setFrequency
        description: Set or update the frequency for the email
        produces:
          - application/json
        parameters:
          - name: user_id
            in: path
            description: ID of user
            required: true
            type: integer
          - name: frequency
            in: query
            description: The chosen frequency in hour of the mail report
            required: true
            type: number
        responses:
          '200':
            description: Ok
          '400':
            description: Bad request, frequency missing

    """