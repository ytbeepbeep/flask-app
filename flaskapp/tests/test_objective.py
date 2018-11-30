from flaskapp.tests.utility import client, login, new_objective, create_user
from flaskapp.database import db, User, Objective
from datetime import datetime, timedelta
from flaskapp.tests.id_parser import get_element_by_id
import requests_mock, requests
import os

DATASERVICE = os.environ['DATA_SERVICE']
OBJECTIVESERVICE = os.environ['OBJECTIVE_SERVICE']


def test_create_objective(client):
    tested_app, app = client

    # test for create_objective having not logged in
    reply = tested_app.post('/create_objective')
    assert reply.status_code == 401
    
    # create a new user
    with requests_mock.mock() as m:
        m.post(DATASERVICE + '/users', json={'user': 1})
        assert create_user(tested_app).status_code == 200

    reply = login(tested_app, email='marco@prova.it', password='123456')
    assert reply.status_code == 200

    # test for create_objective logged in but without data
    reply = tested_app.post('/create_objective')
    assert reply.status_code == 400

    # test for create_objective logged in with wrong data
    reply = tested_app.post('/create_objective', data=dict(
            start_date="asd",
            name="Wrong test1"
    ))
    assert reply.status_code == 400

    reply = tested_app.post('/create_objective', data=dict(
            end_date="asd",
            name="Wrong test2"
    ))
    assert reply.status_code == 400

    reply = tested_app.post('/create_objective', data=dict(
            target_distance=-20,
            name="Wrong test3"
    ))
    assert reply.status_code == 400

    # end date before start date
    reply = tested_app.post('/create_objective', data=dict(
            start_date="2018-07-04",
            end_date="2017-07-04",
            name="Wrong test3"
    ))
    assert reply.status_code == 400

    with requests_mock.mock() as m:
        m.post(OBJECTIVESERVICE + '/objectives')
        reply = tested_app.post('/create_objective', data=dict(
                start_date="2018-07-04",
                end_date="2018-07-05",
                target_distance=22,
                name="Test OK"
        ))
    assert reply.status_code == 200


def test_view_objectives(client):
    tested_app, app = client

    with app.app_context():
        # create a new user
        with requests_mock.mock() as m:
            m.post(DATASERVICE + '/users', json={'user': 1})
            assert create_user(tested_app).status_code == 200

        reply = login(tested_app, email='marco@prova.it', password='123456')
        assert reply.status_code == 200
        
        # add the objective
        obj = new_objective(name="Test1")

        with requests_mock.mock() as m:
            m.get(OBJECTIVESERVICE + '/objectives?user_id=1', json=obj.to_json())
            reply = requests.get(OBJECTIVESERVICE + '/objectives?user_id=1')
            # assert tested_app.get('/objectives', follow_redirects=True).status_code == 200


        # retrieve the objective table
        objectives = db.session.query(Objective) 

        
        # assert reply.status_code == 200

        # for o in objectives.all():
        #     assert get_element_by_id("objective_%s_name"%(o.id), str(reply.data)) == str(o.name)
        #     assert get_element_by_id("objective_%s_start_date"%(o.id), str(reply.data)) == str(o.start_date)
        #     assert get_element_by_id("objective_%s_end_date"%(o.id), str(reply.data)) == str(o.end_date)
        #     assert get_element_by_id("objective_%s_target_distance"%(o.id), str(reply.data)) == str(o.target_distance)
        #     assert get_element_by_id("objective_%s_completion"%(o.id), str(reply.data)) == str(o.completion)
