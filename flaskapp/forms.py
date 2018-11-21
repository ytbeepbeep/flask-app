from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired, Email, NumberRange


class LoginForm(FlaskForm):
    email = f.StringField('Email', validators=[DataRequired("Insert a valid email."), Email()])
    password = f.PasswordField('Password', validators=[DataRequired("Insert your password")])

    display = ['email', 'password']

class UserForm(FlaskForm):
    email = f.StringField('Email', validators=[DataRequired("Insert a valid email."), Email()])
    firstname = f.StringField('Firstname', validators=[DataRequired("Insert your first name.")])
    lastname = f.StringField('Lastname', validators=[DataRequired("Insert your last name")])
    password = f.PasswordField('Password', validators=[DataRequired("Insert a valid password")])
    age = f.IntegerField('Age', validators=[NumberRange(min=0)])
    weight = f.FloatField('Weight')
    max_hr = f.IntegerField('Max_hr')
    rest_hr = f.IntegerField('Rest_hr')
    vo2max = f.FloatField('Vo2max')

    display = ['email', 'firstname', 'lastname', 'password',
               'age', 'weight', 'max_hr', 'rest_hr', 'vo2max']


class DeleteForm(FlaskForm):
    password = f.PasswordField('Password', validators=[DataRequired("Insert a valid password")])
    display = ['password']