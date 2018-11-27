from flaskapp.views.home import home
from flaskapp.views.auth import auth
from flaskapp.views.users import users
from flaskapp.views.run import run
from flaskapp.views.objectives import objectives
from flaskapp.views.statistics import statistics

blueprints = [home, auth, users, objectives, run, statistics]
