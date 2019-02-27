from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(message='Name can not be empty'), Length(6, 12, message='Name can only be between 6~12 characters')])
    password = PasswordField('password', validators=[DataRequired(message='Password can not be empty'), Length(6, 20, message='Password can only be between 6~20 characters')])
    confirm = PasswordField('confirm', validators=[EqualTo('password', message='Inconsistent password')])
    email = StringField('email', validators=[Email(message='Invalid email format')])
    submit = SubmitField('register')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise  ValidationError('The email address is registered by another user')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(message='No empty')])
    password = PasswordField('password', validators=[DataRequired(message='No empty')])
    submit = SubmitField('login')