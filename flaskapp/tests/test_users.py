from flaskapp.tests.utility import client, login, create_user, logout, new_user
from flaskapp.database import db, Credential
from werkzeug.security import check_password_hash
import requests_mock
import os

DATASERVICE = os.environ['DATA_SERVICE']


def test_create_user(client):
    tested_app, app = client

    assert tested_app.get('/create_user').status_code == 200

    assert tested_app.post('/create_user', data=None).status_code == 400

    with requests_mock.mock() as m:
        m.post(DATASERVICE + '/users', json={'user': 1})
        reply = tested_app.post('/create_user', data=dict(email='andrea@prova.it', firstname='andrea', lastname='bongiorno',
                                                          password='123456',
                                                          age=23,
                                                          weight=70,
                                                          max_hr=120,
                                                          rest_hr=60,
                                                          vo2max=99), follow_redirects=True)

    assert reply.status_code == 200  # create_user success (it also redirect to login)

    assert login(tested_app, 'andrea@prova.it', '123456').status_code == 200

    # cannot create a user when already logged in
    assert create_user(tested_app).status_code == 403

    with app.app_context():
        user = db.session.query(Credential).filter(Credential.email == 'andrea@prova.it').first()
        assert user is not None
        assert user.email == 'andrea@prova.it'
        assert check_password_hash(user.password, '123456') is True

    logout(tested_app)

    # cannot create a user with the same email
    with requests_mock.mock() as m:
        m.post(DATASERVICE + '/users', status_code=409)
        reply = tested_app.post('/create_user', data=dict(email='andrea@prova.it', firstname='andrea', lastname='bongiorno',
                                                          password='123456',
                                                          age=23,
                                                          weight=70,
                                                          max_hr=120,
                                                          rest_hr=60,
                                                          vo2max=99), follow_redirects=False)
        assert reply.status_code == 409


def test_delete_user(client):
    tested_app, app = client

    with requests_mock.mock() as m:
        m.post(DATASERVICE + '/users', json={'user': 1})
        reply = create_user(tested_app)  # creates a user with 'marco@prova.it' as email, default
    assert reply.status_code == 200

    reply = login(tested_app, 'marco@prova.it', '123456')
    assert reply.status_code == 200

    reply = logout(tested_app)
    assert reply.status_code == 200

    # retrieve delete_user page without logging in before
    reply = tested_app.get('/delete_user')
    assert reply.status_code == 401

    reply = login(tested_app, email='marco@prova.it', password='123456')
    assert reply.status_code == 200

    # retrieve delete_user page
    reply = tested_app.get('/delete_user')
    assert reply.status_code == 200

    # post bad request
    reply = tested_app.post('/delete_user', data=None)
    assert reply.status_code == 400

    # post incorrect password
    reply = tested_app.post('/delete_user', data=dict(password='000000'))
    assert reply.status_code == 401

    # post correct password and checking that the user has been deleted
    with requests_mock.mock() as m:
        m.delete(DATASERVICE + '/users/1')
        reply = tested_app.post('/delete_user', data=dict(password='123456'), follow_redirects=True)
    assert reply.status_code == 200

    with app.app_context():
        assert db.session.query(Credential).filter(Credential.email == 'marco@prova.it').first() is None

    with app.app_context():
        user1 = new_user()
        user1.dataservice_user_id = 99999
        db.session.add(user1)
        assert login(tested_app, user1.email, 'test').status_code == 200
        with requests_mock.mock() as m:
            m.delete(DATASERVICE + '/users/99999', status_code=404)
            reply = tested_app.post('/delete_user', data=dict(password='test'), follow_redirects=True)
    assert reply.status_code == 404


def test_users_list(client):
    tested_app, app = client

    assert login(tested_app, email='example@example.com', password='admin').status_code == 200

    # only admin can get this page
    assert tested_app.get('/users').status_code == 200

    reply = logout(tested_app)
    assert reply.status_code == 200

    with requests_mock.mock() as m:
        m.post(DATASERVICE + '/users', json={'user': 1})
        assert create_user(tested_app).status_code == 200

    assert login(tested_app, email='marco@prova.it', password='123456').status_code == 200

    # marco@prova.it is not admin
    assert tested_app.get('/users').status_code == 401
