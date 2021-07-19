
from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_migrate import Migrate
from datetime import datetime, date

from app import app
from utils import convert_cyrillic_to_ascii
from utils import slugify, time_delta


db = SQLAlchemy(app)  # ---
migrate = Migrate(app, db)


#====== modesl for projects =============

tasks_executors = db.Table(
    'tasks_executors',
    db.Column('task_id', db.Integer(), db.ForeignKey('task.id')),
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    describe = db.Column(db.Text())
    date_begin = db.Column(db.Date())
    date_end = db.Column(db.Date())
    task_type = db.Column(db.String(20))
    priority = db.Column(db.String(20))
    num_of_hours = db.Column(db.Integer())
    status = db.Column(db.String(50))
    slug = db.Column(db.String(120))

    # =============== links =========================
    # to Project (many to one)
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'))
    # to Journal (one to one)
    journal = db.relationship('Journal', backref='task', uselist=False)
    # to User (many to one)
    manager_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # to User (many to many)
    executors = db.relationship(
        'User',
        secondary=tasks_executors,
        backref=db.backref('executor_tasks', lazy='dynamic'))

    def generate_slug(self):

        if self.title:
            raw_slug = slugify(f'{self.title}-{datetime.now().timestamp()}')
            self.slug = raw_slug if raw_slug.isascii() else convert_cyrillic_to_ascii(raw_slug)

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return f'Task: {self.title}'

    def time_count(self):
        return time_delta(self.date_end - date.today(), str_data=True)

    def take_time(self):
        return time_delta(date.today() - self.date_begin, str_data=True)


class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_spent = db.Column(db.DateTime())

    # =============== links =========================
    # to Task (one to one)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    # to Comment (one to many)
    comments = db.relationship('Comment', backref='journal')

    def comments_sorted(self, reverse=False):
        return sorted(self.comments, key=lambda comment: comment.create_at, reverse=reverse)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    create_at = db.Column(db.DateTime, default=datetime.now())

    # =============== links =========================
    # to User (many to one)
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # to Journal (many to one)
    journal_id = db.Column(db.Integer(), db.ForeignKey('journal.id'))


projects_executors = db.Table('project_executors',
                                        db.Column('project_id', db.Integer(), db.ForeignKey('project.id')),
                                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
                                        )


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    describe = db.Column(db.Text())
    slug = db.Column(db.String(140))
    create = db.Column(db.Date(), default=datetime.today().strftime('%Y-%m-%d'))

    # =============== links =========================
    # to Task (one to many)
    tasks = db.relationship('Task', backref='project')
    # to User (many to one)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # to User (many-to-many)
    executors = db.relationship(
        'User',
        secondary=projects_executors,
        backref=db.backref('executor_projects', lazy='dynamic')
    )

    def generate_slug(self):

        if self.title:
            raw_slug = slugify(f'{self.title}-{datetime.now().timestamp()}')
            self.slug = raw_slug if raw_slug.isascii() else convert_cyrillic_to_ascii(raw_slug)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return f'Project: {self.title}'

# ===== models for flask-security =======


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    birthday = db.Column(db.Date)
    position = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean)
    avatar = db.Column(db.LargeBinary)
    slug = db.Column(db.String(150), unique=True)

    # =============== links =========================
    # to Role (many to many)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))
    # to Project (one to many)
    manager_projects = db.relationship('Project', backref='manager')
    # to Task (one to many)
    manager_tasks = db.relationship('Task', backref='manager')
    # to Comment (one to many)
    comments = db.relationship('Comment', backref='author')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.email:
            raw_slug = slugify(f'{self.email}-{datetime.now().timestamp()}')
            self.slug = raw_slug if raw_slug.isascii() else convert_cyrillic_to_ascii(raw_slug)

    def __repr__(self):
        return f'{self.position}: {self.name} {self.surname}'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'{self.name}'
