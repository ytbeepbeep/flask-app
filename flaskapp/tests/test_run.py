import requests
import requests_testing
import requests_mock
import os
from flaskapp.database import db
from flaskapp.tests.utility import client, create_user, login
from flaskapp.tests.id_parser import get_element_by_id

from flaskapp.services import DataService

DATASERVICE = os.environ['DATA_SERVICE']


def test_run(client):
    tested_app, app = client

    # Run with id 1
    run1 = {
        "id": 1,
        "start_date": "2018-10-10",
        "distance": "22",
        "elapsed_time": "33",
        "average_speed": "32",
        "average_heartrate": "1",
        "total_elevation_gain": "1"
    }
    url = "http://0.0.0.0:5001/run/1"
    requests_testing.add(request={'url': url}, response=run1)

    # prepare the database creating a new user
    with requests_mock.mock() as m:
        m.post(DATASERVICE + '/users', json={'user': 1})
        reply = create_user(tested_app)  # creates a user with 'marco@prova.it' as email, default
    assert reply.status_code == 200

    # login as new user
    reply = login(tested_app, email='marco@prova.it', password='123456')
    assert reply.status_code == 200

    """# retrieve the user object from db
    with app.app_context():
        # retrieve run page
        run = tested_app.get('http://0.0.0.0:5001/run/1')  # should be one, because the database is empty
        assert run.status_code == 200

        # check the correctness of the fields
        assert get_element_by_id('start_date', str(reply.data)) == str(run.start_date)
        assert get_element_by_id('distance', str(reply.data)) == str(run.distance)
        assert get_element_by_id('elapsed_time', str(reply.data)) == str(run.elapsed_time // 60)
        assert get_element_by_id('average_speed', str(reply.data)) == str(run.average_speed)
        assert get_element_by_id('average_heartrate', str(reply.data)) == str(run.average_heartrate)
        assert get_element_by_id('total_elevation_gain', str(reply.data)) == str(run.total_elevation_gain)

        # retrieving not existing run
        reply = tested_app.get('/run/45678')
        assert reply.status_code == 404
    """
