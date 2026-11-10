from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,  EmailField
from wtforms.validators import InputRequired, Length
from flask_wtf.csrf import CSRFProtect

class LoginForm(FlaskForm):
    email = EmailField('Name', validators=[InputRequired(), Length(min=5, max=25, message='Username must be in 5 to 25 characters')])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=5, max=25, message='Username must be in 5 to 25 characters')])
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[InputRequired()])
    
