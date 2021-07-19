from wtforms import StringField, TextAreaField, SelectMultipleField, SelectField, IntegerField, SubmitField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired

from models import User


class SelectMultipleFieldWithoutValidate(SelectMultipleField):

    def __init__(self, *args, **kwargs):
        super(SelectMultipleFieldWithoutValidate, self).__init__(*args, **kwargs)

    def pre_validate(self, form):
        pass


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    manager = SelectField('Manager', choices=[(i.id, f'{i.name} {i.surname}') for i in User.query.all()])
    executors = SelectMultipleFieldWithoutValidate('Executors',
                                                   choices=[(i.id, f'{i.name} {i.surname}') for i in User.query.all()])
    describe = TextAreaField('Describe')
    submit = SubmitField('Submit')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    date_begin = DateField('The date of the beginning', validators=[InputRequired()])
    date_end = DateField('Completion date', validators=[InputRequired()])
    task_type = SelectField('Type of task', choices=[('Feature', 'Feature'), ('Bug', 'Bug')])
    priority = SelectField('Task priority',
                           choices=[('Normal', 'Normal'), ('High', 'High'), ('Immediately', 'Immediately')])
    num_of_hours = IntegerField('Number of hours per task')
    manager = SelectField('Manager of task',
                          choices=[(i.id, f'{i.name} {i.surname}') for i in User.query.all()])
    executors = SelectMultipleFieldWithoutValidate('Executor of task',
                                                   choices=[(i.id, f'{i.name} {i.surname}') for i in User.query.all()])
    status = SelectField('Status of task',
                         choices=[('Done', 'Done'), ('In work', 'In work'), ('On finalize', 'On finalize')],
                         default='In work')
    describe = TextAreaField('Describe')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = TextAreaField('Add comment')
    submit = SubmitField('Create new comment')
