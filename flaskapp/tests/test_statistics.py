from flaskapp.tests.utility import client, create_user, login
from flaskapp.tests.id_parser import get_element_by_id

import os
import requests_mock
import requests

DATASERVICE = os.environ['DATA_SERVICE']

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

runs = [
        {
            "average_heartrate": None, 
            "average_speed": 2, 
            "description": None, 
            "distance": 1, 
            "elapsed_time": 78, 
            "id": 1, 
            "runner_id": 1, 
            "start_date": 1541697617.0, 
            "strava_id": 1953352080, 
            "title": "Evening Run", 
            "total_elevation_gain": 0.0
        }, 
        {
            "average_heartrate": None, 
            "average_speed": 2, 
            "description": None, 
            "distance": 2, 
            "elapsed_time": 27, 
            "id": 2, 
            "runner_id": 1, 
            "start_date": 1541428619.0, 
            "strava_id": 1947486973, 
            "title": "Test 2", 
            "total_elevation_gain": 0.0
            },             {
            "average_heartrate": None, 
            "average_speed": 2, 
            "description": None, 
            "distance": 3, 
            "elapsed_time": 16, 
            "id": 3, 
            "runner_id": 1, 
            "start_date": 1541427162.0, 
            "strava_id": 1947454690, 
            "title": "Test 1", 
            "total_elevation_gain": 0.0
        }
    ]


def test_statistics_unauthorized(client):
    tested_app, app = client

    # Try to get the page without login
    response = tested_app.get('/statistics')
    assert response.status_code == 401


def test_statistics(client):
    tested_app, app = client

    with requests_mock.mock() as mock:
        # Login the user first
        mock.post(DATASERVICE + '/users', json={'user': user_id})
        response = tested_app.post('/create_user', data=user, follow_redirects=True)
        assert response.status_code == 200 # User successfully created

        assert login(tested_app, user['email'], user['password']).status_code == 200

        # Mock user and runs
        mock.get(DATASERVICE + '/users/%s' % user_id, json=user)
        mock.get(DATASERVICE + '/runs', json=runs)

        response = tested_app.get('/statistics')
        assert response.status_code == 200

        for run in runs:
            assert get_element_by_id("run_%s" % run['id'], str(response.data)) == run['title']


def test_statistics_error(client):
    tested_app, app = client

    with requests_mock.mock() as mock:
        mock.post(DATASERVICE + '/users', json={'user': user_id})
        response = tested_app.post('/create_user', data=user, follow_redirects=True)
        assert response.status_code == 200 # User successfully created

        assert login(tested_app, user['email'], user['password']).status_code == 200

        mock.get(DATASERVICE + "/runs", exc=requests.exceptions.ConnectTimeout)

        response = tested_app.get('/statistics')
        assert response.status_code == 500

