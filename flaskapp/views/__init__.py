from flaskapp.views.home import home
from flaskapp.views.auth import auth
from flaskapp.views.users import users
from flaskapp.views.run import run
from flaskapp.views.objectives import objectives
from flaskapp.views.statistics import statistics
from flaskapp.views.challenges import challenges
from flaskapp.views.report import report

blueprints = [home, auth, users, objectives, run, statistics, challenges, report]
