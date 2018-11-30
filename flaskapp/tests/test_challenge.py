import requests_mock
import os
from flaskapp.tests.utility import client, create_user, login
from flaskapp.tests.id_parser import get_element_by_id

DATASERVICE = os.environ['DATA_SERVICE']
CHALLENGESERVICE = os.environ['CHALLENGE_SERVICE']

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

# Run with id 1
run1 = {
    "id": 1,
    "name": "test_run",
    "start_date": "2018-10-10",
    "distance": "22",
    "elapsed_time": "33",
    "average_speed": "32",
    "average_heartrate": "1",
    "total_elevation_gain": "1"
}

# Run with id 2
run2 = {
    "id": 2,
    "name": "test_run_two",
    "start_date": "2018-10-11",
    "distance": "24",
    "elapsed_time": "40",
    "average_speed": "30",
    "average_heartrate": "1",
    "total_elevation_gain": "1"
}

challenge = {
    "user_id": 1,
    "run_one": 1,
    "name_run_one": "test_run",
    "run_two": 2,
    "name_run_two": "test_run_two"
}


def test_run(client):
    tested_app, app = client

    # prepare the database creating a new user
    with requests_mock.mock() as m:
        m.post(DATASERVICE + '/users', json={'user': 1})
        m.get(DATASERVICE + '/runs/1', json=run1)
        m.get(DATASERVICE + '/runs/2', json=run2)
        reply = create_user(tested_app)  # creates a user with 'marco@prova.it' as email, default
        assert reply.status_code == 200

        # login as new user
        reply = login(tested_app, email='marco@prova.it', password='123456')
        assert reply.status_code == 200

        reply = tested_app.get('/run/1')
        assert reply.status_code == 200

        reply = tested_app.get('/run/2')
        assert reply.status_code == 200

        m.get(DATASERVICE + '/runs/4', status_code=500)
        reply = tested_app.get('/run/4')
        assert reply.status_code == 500

        m.get(CHALLENGESERVICE + '/challenges?user_id=1', json=challenge)
        reply = tested_app.get('/challenges?user_id=1')
        assert reply.status_code == 200

        m.post(CHALLENGESERVICE + '/challenges', json=challenge)
        reply = tested_app.post('/challenges', json=challenge)
        assert reply.status_code == 405

        m.post(CHALLENGESERVICE + '/challenges?user_id=1', json=user)
        reply = tested_app.post('/challenges?user_id=1', json=user)
        assert reply.status_code == 405

        m.post(CHALLENGESERVICE + '/challenges', json=user)
        reply = tested_app.post('/challenges', json=user)
        assert reply.status_code == 405

        m.get(CHALLENGESERVICE + '/challenges/1?user_id=1', json=challenge)
        assert tested_app.get('/challenges/1').status_code == 200


def test_challenge_not_found(client):
    tested_app, app = client

    with requests_mock.mock() as m:
        m.post(DATASERVICE + '/users', json={'user': user_id})
        response = tested_app.post('/create_user', data=user, follow_redirects=True)
        assert response.status_code == 200  # User successfully created

        assert login(tested_app, user['email'], user['password']).status_code == 200

        m.get(CHALLENGESERVICE + "/challenges/-1", status_code=500)
        assert tested_app.get('challenges/-1').status_code == 500



