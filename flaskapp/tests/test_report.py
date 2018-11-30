from flaskapp.tests.utility import client, create_user, login
from flaskapp.tests.id_parser import get_element_by_id

import os
import requests_mock
import requests

DATASERVICE = os.environ['DATA_SERVICE']
MAIL_SERVICE_URL = os.environ['MAIL_SERVICE']

user_id = 1
user = dict(
    email='test@test.com', 
    firstname='test',
    lastname='user',
    password='test',
    age=42,
    weight=42,
    max_hr=42,
    rest_hr=42,
    vo2max=42)


def test_set_frequency(client):
    tested_app, app = client

    with requests_mock.mock() as mock:
        # Login the user first
        mock.post(DATASERVICE + '/users', json={'user': user_id})
        response = tested_app.post('/create_user', data=user, follow_redirects=True)
        assert response.status_code == 200 # User successfully created

        assert login(tested_app, user['email'], user['password']).status_code == 200

        freq = 1

        # Mock frequency
        mock.get(MAIL_SERVICE_URL + '/frequency/%s' % user_id, json={'frequency': freq})

        response = tested_app.get('/frequency')
        assert response.status_code == 200


def test_report_unauthorized(client):
    tested_app, app = client

    # Try to get the page without login
    response = tested_app.get('/frequency')
    assert response.status_code == 401


def test_frequency_error(client):
    tested_app, app = client

    with requests_mock.mock() as mock:
        mock.post(DATASERVICE + '/users', json={'user': user_id})
        response = tested_app.post('/create_user', data=user, follow_redirects=True)
        assert response.status_code == 200 # User successfully created

        assert login(tested_app, user['email'], user['password']).status_code == 200

        mock.post(MAIL_SERVICE_URL + '/frequency/%s' % user_id, status_code=500)

        response = tested_app.post('/frequency', data={"setting_mail":6})
        assert response.status_code == 500

