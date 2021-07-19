from wtforms import Form, widgets, StringField, TextField, SelectField, SelectMultipleField
from wtforms import PasswordField, BooleanField, FileField, SubmitField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired, Length

from models import Role


class UserForm(FlaskForm):
    name = StringField('Name', validators=[
        Length(min=2, max=50, message='Password must be between twenty five characters')
    ])
    surname = StringField('Surname', validators=[DataRequired(message='Surname must required')])
    birthday = DateField('Birthday')
    position = StringField('Position')
    email = EmailField('Email', validators=[Email('Incorrect email '), DataRequired(message='Email must required')])
    password = PasswordField('New password', validators=[
        Length(min=4, max=25, message='Password must be between twenty five characters')])
    password2 = PasswordField('Repeat password', validators=[
        DataRequired(message='Surname must required'),
        EqualTo('password', message='Password must much'),
    ])
    active = SelectField('Is active', choices=[(True, 'Active'), (False, 'Deactivated')])
    # avatar = FileField('Avatar')
    roles = SelectField('Role', choices=[(i.name, i.name) for i in Role.query.all()])
    submit = SubmitField('Submit')
