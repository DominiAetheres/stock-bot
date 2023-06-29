from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class Login(FlaskForm):
    """
    A FlaskForm representing the login form.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class Registration(FlaskForm):
    """
    A FlaskForm representing the user registration form.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message="Your passwords must match.")])
    submit = SubmitField('Register')

    def validateUsername(self, username):
        """
        Validates that the username entered is unique. 
        Raises a `ValidationError` if it already exists.
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken :(")

    def validate_email(self, email):
        '''
        Validates that the email entered is unique. 
        Raises a `ValidationError` if it already exists.
        '''
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('You have already registered with this email.')
