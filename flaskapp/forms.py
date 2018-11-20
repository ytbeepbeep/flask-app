from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = f.StringField('Email', validators=[DataRequired("Insert a valid email."), Email()])
    password = f.PasswordField('Password', validators=[DataRequired("Insert your password")])

    display = ['email', 'password']
