from flask import Flask
from flaskapp.views import blueprints


def create_app():
    app = Flask(__name__)

    # App
    # TODO: What the hell! Are they needed? And why we use 'A SECRET KEY'?
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        blueprint.app = app

    return app


def main():
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == '__main__':
    main()
