import requests
import requests_testing
import requests_mock
import os
from flaskapp.database import db
from flaskapp.tests.utility import client, create_user, login
from flaskapp.tests.id_parser import get_element_by_id

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

def test_run(client):
    tested_app, app = client

    # prepare the database creating a new user
    with requests_mock.mock() as m:
        m.post(DATASERVICE + '/users', json={'user': 1})
        m.get(DATASERVICE + '/runs/1', json=run1)
        reply = create_user(tested_app)  # creates a user with 'marco@prova.it' as email, default
        assert reply.status_code == 200

        # login as new user
        reply = login(tested_app, email='marco@prova.it', password='123456')
        assert reply.status_code == 200

        reply = tested_app.get('/run/1')
        assert reply.status_code == 200

        assert get_element_by_id("run_name", str(reply.data)) == ("Run: %s" % run1['name'])


def test_run_not_found(client):
    tested_app, app = client

    with requests_mock.mock() as mock:
        mock.post(DATASERVICE + '/users', json={'user': user_id})
        response = tested_app.post('/create_user', data=user, follow_redirects=True)
        assert response.status_code == 200 # User successfully created

        assert login(tested_app, user['email'], user['password']).status_code == 200
        
        mock.get(DATASERVICE + "/runs/-1", status_code=404)
        assert tested_app.get('runs/-1').status_code == 404

