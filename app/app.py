from flask import Flask, redirect, url_for, request
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user
from wtf_tinymce import wtf_tinymce
from flask_mail import Mail, Message

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

# ####### SQLAlchemy #######
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from models import *

####### Flask Admin#######
# admin = Admin(app)


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    """
    Класс для ограничения доступа к моделям в админке
    """
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    """
    Класс для блокировки доступа к корневой директории /admin
    """
    pass


class UserAdminView(AdminMixin, BaseModelView):
    #form_columns = ['tags', 'title', 'body']
    pass


class ProjectAdminView(AdminMixin, BaseModelView):
    #form_columns = ['tags', 'title', 'body']
    pass


class TaskAdminView(AdminMixin, BaseModelView):
    #form_columns = ['tags', 'title', 'body']
    pass


class RoleAdminView(AdminMixin, BaseModelView):
    # form_columns = ['posts', 'name']
    pass


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(ProjectAdminView(Project, db.session))
admin.add_view(TaskAdminView(Task, db.session))
admin.add_view(RoleAdminView(Role, db.session))

####### Flask-Security #######
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

######## TinyMCE #######
wtf_tinymce.init_app(app)

####### Flask_Mail #######
mail = Mail(app)

