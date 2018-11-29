from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from datetime import datetime, date
import calendar


db = SQLAlchemy()


class Credential(db.Model):
    __tablename__ = 'credential'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    password = db.Column(db.Unicode(128), nullable=False)
    dataservice_user_id = db.Column(db.Integer, nullable=False)
    authorized_strava = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    is_anonymous = False

    def __init__(self, *args, **kw):
        super(Credential, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        print(password, " ", self.password)
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id

    def __str__(self):
        return "%s - %s - authorized_strava: %s (authenticated? %s)"%(self.id, self.email, self.authorized_strava, self.is_authenticated)


# DO NOT INSERT USER IN THIS TABLE! THIS SERVES ONLY TO SHORTEN CODE IN SOME SITUATION. E.G. LIKE USER CREATION
class User(db.Model):  # pragma: no cover
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    strava_token = db.Column(db.String(128))
    age = db.Column(db.Integer)
    weight = db.Column(db.Numeric(4, 1))
    max_hr = db.Column(db.Integer)
    rest_hr = db.Column(db.Integer)
    vo2max = db.Column(db.Numeric(4, 2))

    def to_json(self):
        res = {}
        for attr in ('id', 'email', 'firstname', 'lastname', 'age', 'weight',
                     'max_hr', 'rest_hr', 'vo2max'):
            value = getattr(self, attr)
            if isinstance(value, db.Numeric):
                value = float(value)
            res[attr] = value
        return res

# DO NOT INSERT USER IN THIS DB! THIS SERVES ONLY TO SHORTEN CODE IN SOME SITUATION. E.G. LIKE Objective CREATION
class Objective(db.Model): # pragma: no cover
    __tablename__ = 'objective'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    target_distance = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)

    @staticmethod
    def to_datetime(date_str):
        return datetime.fromtimestamp(float(date_str))

    def to_json(self):
        res = {}
        for attr in ('id', 'name', 'target_distance', 'start_date',
                     'end_date', 'user_id'):
            value = getattr(self, attr)
            if isinstance(value, date):
                value = calendar.timegm(value.timetuple())
            res[attr] = value
        return res


class Challenge(db.Model): # pragma: no cover
    __tablename__ = 'challenge'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    run_one = db.Column(db.Integer)
    name_run_one = db.Column(db.Unicode(128))
    run_two = db.Column(db.Integer)
    name_run_two = db.Column(db.Unicode(128))
    id_user = db.Column(db.Integer)

    def set_challenge_user(self,id_usr):
        self.id_user = id_user

    def set_challenge1_run(self,run_one):
        self.run_one = run_one

    def set_challenge2_run(self,run_two):
        self.run_two = run_two

    def set_challenge1_name(self,name_one):
        self.name_run_one = name_one

    def set_challenge2_name(self,name_two):
        self.name_run_two = name_two

    def to_json(self):
        res = {}
        for attr in ('id', 'run_one', 'name_run_one', 'run_two',
                     'name_run_two', 'id_user'):
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            res[attr] = value
        return res


class Report(db.Model):  # pragma: no cover
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    runner_id = db.Column(db.Integer)
    timestamp = db.Column(db.Float)
    frequency = db.Column(db.Float)

    def set_user(self, id_usr):
        self.runner_id = id_usr

    # timestamp from previous report, in seconds                                                                                                                             
    def set_timestamp(self):
        self.timestamp = time()

    # frequency preference stored in seconds                                                                                                                                 
    def set_frequency(self, choice):
        self.frequency = (float(choice)*3600.0)

    def to_json(self):
        res = {}
        for attr in ('id', 'runner_id', 'timestamp', 'frequency'):
            res[attr] = getattr(self, attr)
        return res

