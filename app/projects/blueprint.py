from flask import Blueprint, request, flash, redirect, url_for
from flask import render_template
from flask_security.decorators import roles_accepted
from flask_security import current_user
from sqlalchemy import union_all
from flask_sqlalchemy import BaseQuery

from models import db, Project, User, Journal, Task, Comment
from .forms import ProjectForm, TaskForm, CommentForm

from app import mail, Message

projects = Blueprint('projects', __name__, template_folder='templates')


@projects.route('/')
def index():
    q = request.args.get('q')
    num_page = request.args.get('q')

    if num_page and num_page.isdigit():
        num_page = str(num_page)
    else:
        num_page = 1
    if q:
        filter_a = Project.query.filter(
            Project.title.contains(q) | Project.describe.contains(q)).filter(Project.manager==current_user)
        filter_b = Project.query.filter(
            Project.title.contains(q) | Project.describe.contains(q)).filter(Project.executors.contains(current_user))
        project_objects = filter_a.union_all(filter_b)
    else:
        filter_a = Project.query.order_by(Project.create.desc()).filter(Project.manager==current_user)
        filter_b = Project.query.order_by(Project.create.desc()).filter(Project.executors.contains(current_user))
        project_objects = filter_a.union_all(filter_b)

    pages = project_objects.paginate(page=num_page, per_page=7)

    if q and not pages.items:
        flash('No matches', 'error')
    elif q:
        flash(f'Found {len(pages.items)} matches', 'confirm')

    return render_template('projects/index.html', pages=pages)


@projects.route('/project_detail/<slug>')
@roles_accepted('admin', 'execut')
def project_detail(slug):
    project_object = Project.query.filter(Project.slug==slug).first()

    return render_template('projects/project_detail.html', project=project_object)


@projects.route('/project_create', methods=['POST', 'GET'])
@roles_accepted('admin')
def project_create():
    form = ProjectForm()
    form.manager.data = str(current_user.id)

    if form.validate_on_submit():
        manager = User.query.filter(User.id==current_user.id).first()
        list_executors = [i for i in request.form.getlist('executors')]
        executors = User.query.filter(User.id.in_(list_executors)).all()
        title = request.form.get('title')
        describe = request.form.get('describe')

        if title:
            try:
                project = Project(title=title, describe=describe)
                project.executors.extend(executors)
                project.manager = manager
                db.session.add(project)
                db.session.commit()

                mails = [i.email for i in executors]
                mails.append(manager.email)
                msg = Message('Created new task', recipients=mails)
                msg.body = render_template('projects/mail_project_detail.html', project=project)
                msg.html = render_template('projects/mail_project_detail.html', project=project)
                mail.send(msg)

                flash(f'Project {project.title} successful created', 'confirm')
            except Exception:
                flash("Project didn't create", 'error')

            return redirect(url_for('projects.index'))
    return render_template('projects/project_create.html', form=form)


@projects.route('/project_edit/<slug>', methods=['POST', 'GET'])
@roles_accepted('admin')
def project_edit(slug):
    project_object = Project.query.filter(Project.slug == slug).first()
    form_object = ProjectForm(obj=project_object)

    if form_object.validate_on_submit():
        form_object = ProjectForm(formdata=request.form, obj=project_object)
        form_object.manager.data = User.query.filter(User.id==form_object.manager.data).first()
        form_object.executors.data = User.query.filter(User.id.in_(form_object.executors.data)).all()

        try:
            form_object.populate_obj(project_object)
            db.session.commit()
            flash(f'Project {project_object.title} successful edit', 'confirm')
        except Exception:
            flash('Project not edited', 'error')
        return redirect(url_for('projects.project_detail', slug=project_object.slug))

    current_executors = [i.id for i in project_object.executors]
    current_manager = project_object.manager.id if project_object.manager != None else 1

    return render_template(
        'projects/project_edit.html',
        project=project_object,
        def_ex=current_executors,
        def_man=current_manager,
        form=form_object)


@projects.route('/project_delete/<slug>', methods=['GET', 'POST'])
@roles_accepted('admin')
def project_delete(slug):
    project_object = Project.query.filter(Project.slug == slug).first()
    form_object = ProjectForm(obj=project_object)
    current_executors = [i.id for i in project_object.executors]
    current_manager = project_object.manager.id if project_object.manager != None else 1
    if request.method == 'POST':
        try:
            name = project_object.title
            db.session.delete(project_object)
            db.session.commit()
            flash(f'Project "{name}" successful deleted', 'confirm')
        except Exception:
            flash('Project is not deleted', 'error')
        return redirect(url_for('projects.index'))
    return render_template(
        'projects/project_delete.html',
        project=project_object,
        def_ex=current_executors,
        def_man=current_manager,
        form=form_object)


@projects.route('/task_create/<slug>', methods=['POST', 'GET'])
@roles_accepted('admin')
def task_create(slug):
    project = Project.query.filter(Project.slug==slug).first()
    task_form = TaskForm()
    task_form.submit.label.text = 'Create task'
    task_form.manager.data = str(current_user.id)
    if task_form.validate_on_submit():
        try:
            task = Task(
                title=request.form.get('title'),
                describe=request.form.get('describe'),
                date_begin=request.form.get('date_begin'),
                date_end=request.form.get('date_end'),
                task_type=request.form.get('task_type'),
                priority=request.form.get('priority'),
                num_of_hours=int(request.form.get('num_of_hours')),
                status=request.form.get('status')
            )
            manager = User.query.filter(User.id == current_user.id).first()
            list_executors = [i for i in request.form.getlist('executors')]
            executors = User.query.filter(User.id.in_(list_executors)).all()
            task.manager = manager
            task.executors.extend(executors)
            journal = Journal(time_spent=task.date_begin)
            db.session.add_all([task, journal])
            db.session.commit()
            project.tasks.append(task)
            task.journal = journal
            db.session.add_all([task, project])
            db.session.commit()
            flash(f'Task {task.title} successful created', 'confirm')
        except Exception:
            flash("Task didn't created", 'error')

        return redirect(url_for('projects.project_detail', slug=project.slug))
    return render_template('projects/task_create.html', project=project, form=task_form)


@projects.route('/task_detail/<slug>', methods=['GET', 'POST'])
def task_detail(slug):
    task_object = Task.query.filter(Task.slug==slug).first()
    comment_form = CommentForm()
    if comment_form.validate_on_submit and request.method == 'POST':
        try:
            comment_object = Comment(body=request.form.get('body'))
            db.session.add(comment_object)
            db.session.commit()
            journal_object = task_object.journal
            author = current_user
            comment_object.author = author
            journal_object.comments.append(comment_object)
            db.session.add_all([comment_object, journal_object])
            db.session.commit()
            flash('New comment successful created', 'confirm')
        except Exception:
            flash("Comment didn't created", "error")
        return redirect(url_for('projects.task_detail', slug=task_object.slug))

    return render_template('projects/task_detail.html', task=task_object, form=comment_form)


@projects.route('/task_edit/<slug>', methods=['POST', 'GET'])
def task_edit(slug):
    task_object = Task.query.filter(Task.slug == slug).first()
    form_object = TaskForm(obj=task_object)
    if form_object.validate_on_submit():
        form_object = TaskForm(formdata=request.form, obj=task_object)
        form_object.manager.data = User.query.filter(User.id == form_object.manager.data).first()
        form_object.executors.data = User.query.filter(User.id.in_(form_object.executors.data)).all()

        try:
            form_object.populate_obj(task_object)
            db.session.commit()
            flash(f'Task "{task_object.title}" successful edit', 'confirm')
        except Exception:
            flash('Task not edited', 'error')
        return redirect(url_for('projects.task_detail', slug=task_object.slug))

    current_executors = [i.id for i in task_object.executors]
    current_manager = task_object.manager.id if task_object.manager != None else 1

    return render_template(
        'projects/task_edit.html',
        task=task_object,
        def_ex=current_executors,
        def_man=current_manager,
        form=form_object)


@projects.route('/check_template')
def check_template():
    project = Project.query.filter(Project.title=='First project').first()

    return render_template('projects/mail_project_detail.html', project=project)
