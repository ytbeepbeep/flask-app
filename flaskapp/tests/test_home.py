from flaskapp.tests.utility import client, create_user, login, logout


def test_home(client):
    tested_app, app = client

    # User not authenticated
    response = client.get('/')
    assert b'Hi Anonymous!' in response.data

    # Log in the user
    assert login(tested_app, 'test@test', 'ciao').status_code == 200

    response = client.get('/')
    assert b'Your last 10 runs' in response.data
