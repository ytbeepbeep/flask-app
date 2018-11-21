from flaskapp.views.home import home
from flaskapp.views.auth import auth
from flaskapp.views.users import users

blueprints = [home, auth, users]
