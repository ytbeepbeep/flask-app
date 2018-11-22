from flaskapp.views.home import home
from flaskapp.views.auth import auth
from flaskapp.views.users import users
from flaskapp.views.run import run

blueprints = [home, auth, users, run]
