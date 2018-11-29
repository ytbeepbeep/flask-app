from flaskapp.tests.utility import client, create_user, login, logout
from flaskapp.tests.id_parser import get_element_by_id
from flaskapp.database import db, Credential

import os
import requests_mock

DATASERVICE = os.environ['DATA_SERVICE']


def test_home(client):
    tested_app, app = client

    # User not authenticated
    response = tested_app.get('/')
    assert response.status_code == 200
    assert b'Hi Anonymous!' in response.data

    # Log in the user
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
            }, 
            {
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

    with requests_mock.mock() as mock:
        # Login the user first
        mock.post(DATASERVICE + '/users', json={'user': user_id})
        response = tested_app.post('/create_user', data=user, follow_redirects=True)
        assert response.status_code == 200 # User successfully created

        # Mock users and runs
        mock.get(DATASERVICE + '/users/%s' % user_id, json=user)
        mock.get(DATASERVICE + '/runs', json=runs)
    
        assert login(tested_app, user['email'], user['password']).status_code == 200

        response = tested_app.get('/')
        assert response.status_code == 200

        # Test without set the strava token
        assert get_element_by_id("strava_auth_btn", str(response.data)) is not None

        # Set the strava token and try again
        with app.app_context():
            credential = db.session.query(Credential).filter(Credential.email == user['email']).first()
            credential.authorized_strava = True
            db.session.add(credential)
            db.session.commit()

        response = tested_app.get('/')
        assert response.status_code == 200

        assert get_element_by_id("title", str(response.data)) == "Hi %s" % user['firstname']

        assert get_element_by_id("total_average_speed", str(response.data)) == "2.0"

        for run in runs:
            print("run_%s" % run['id'])
            assert get_element_by_id("run_%s" % run['id'], str(response.data)) == run['title']

