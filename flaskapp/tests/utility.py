import pytest
import os
import tempfile
from flaskapp.app import create_app
from flaskapp.database import db, Credential


@pytest.fixture
def client():
    """ This function initialize a new DB for every test and creates the app. This function returns a tuple,
    the first element is a test client and the second is the app itself. Test client must be used for sending
    request and the app should be used for getting a context when, for example, we need to query the DB.
    I haven't found a more elegant way to do this."""
    app = create_app()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+app.config['DATABASE']
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF validation -> DO THIS ONLY DURING TESTS!

    client = app.test_client()

    db.create_all(app=app)
    db.init_app(app=app)
    with app.app_context():
        q = db.session.query(Credential).filter(Credential.email == 'example@example.com')
        credential = q.first()
        if credential is None:
            example = Credential()
            example.email = 'example@example.com'
            example.is_admin = True
            example.set_password('admin')
            example.user_id = -1
            db.session.add(example)
            db.session.commit()

    yield client, app

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def login(client, email, password):
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def create_user(client, email='marco@prova.it', firstname='marco', lastname='mario', password='123456', age=18,
                weight=70, max_hr=120, rest_hr=65, vo2max=99):

    return client.post('/create_user', data=dict(email=email,
                                                 firstname=firstname,
                                                 lastname=lastname,
                                                 password=password,
                                                 age=age,
                                                 weight=weight,
                                                 max_hr=max_hr,
                                                 rest_hr=rest_hr,
                                                 vo2max=vo2max), follow_redirects=True)


def new_user():
    credential = Credential()
    credential.email = 'test@example.com'
    credential.set_password('test')
    db.session.add(credential)
    db.session.commit()
    return credential
