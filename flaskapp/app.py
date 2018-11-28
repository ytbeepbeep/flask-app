import os
from flask import Flask
from flaskapp.views import blueprints
from flaskapp.auth import login_manager
from flaskapp.database import db, Credential



def create_app():
    app = Flask(__name__)

    # App
    # TODO: What the hell! Are they needed? And why we use 'A SECRET KEY'?
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beepbeep.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['STRAVA_CLIENT_ID'] = os.environ['STRAVA_CLIENT_ID']
    app.config['STRAVA_CLIENT_SECRET'] = os.environ['STRAVA_CLIENT_SECRET']

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        blueprint.app = app

    db.init_app(app)
    db.create_all(app=app)
    login_manager.init_app(app)

    # create a first admin user
    with app.app_context():
         q = db.session.query(Credential).filter(Credential.email == 'example@example.com')
         user_credential = q.first()
         if user_credential is None:
             example = Credential()
             example.email = 'example@example.com'
             example.is_admin = True
             example.dataservice_user_id = -1
             example.set_password('admin')
             db.session.add(example)
             db.session.commit()
    return app


def main():
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == '__main__':
    main()
