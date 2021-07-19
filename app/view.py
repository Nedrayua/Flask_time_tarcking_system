from app import app
from flask import render_template, request, flash, redirect, url_for

from models import User, Role, db
from forms import UserForm
from app import user_datastore
from app import mail, Message


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/users')
def users_view():
    q = request.args.get('q')

    num_page = request.args.get('page')
    if num_page and num_page.isdigit():
        num_page = int(num_page)
    else:
        num_page = 1

    if q:
        users_objects = User.query.filter(User.name.contains(q) | User.surname.contains(q))
    else:
        users_objects = User.query.order_by(User.name.desc())

    pages = users_objects.paginate(page=num_page, per_page=7)

    if q and not pages.items:
        flash('No matches', 'error')
    elif q:
        flash(f'Found {len(pages.items)} matches', 'confirm')

    return render_template('users.html', pages=pages, users=users_objects)


@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form_object = UserForm()

    # if request.method == 'POST':
    if form_object.validate_on_submit():
        name = request.form['name']
        surname = request.form['surname']
        birthday = request.form['birthday']
        position = request.form['position']
        email = request.form['email']
        password = request.form['password']
        active = True if request.form['active'] == 'True' else False
        #avatar = request.form['avatar']
        roles = request.form['roles']
        if email and password:
            try:
                role = user_datastore.find_role(role=roles)
                user = user_datastore.create_user(
                    name=name,
                    surname=surname,
                    birthday=birthday,
                    position=position,
                    email=email,
                    password=password,
                    active=active
                )
                user_datastore.add_role_to_user(user, role)
                db.session.commit()
                flash(f'User {user.name} {user.surname} successful created', 'confirm')
            except Exception:
                flash('Something do wrong', 'error')

        return redirect(url_for('users_view'))
    return render_template('create_user.html', form=form_object)



@app.route('/user_detail/<slug>', methods=['POST', 'GET'])
def user_detail(slug):
    user_object = User.query.filter(User.slug==slug).first()

    return render_template('user_detail.html', user=user_object)


@app.route('/edit_user/<slug>', methods=['POST', 'GET'])
def edit_user(slug):
    user_object = User.query.filter(User.slug==slug).first()

    if request.method == 'POST':
        user_form = UserForm(formdata=request.form, obj=user_object)

        user_form.active.data = True if user_form.active.data == 'True' else False
        role = user_datastore.find_role(role=user_form.roles.data)
        user_form.roles.data = [role]
        user_form.birthday.data = request.form['birthday']

        user_form.populate_obj(user_object)
        db.session.commit()
        flash('User successful edit', 'confirm')
        return redirect(url_for('user_detail', slug=user_object.slug))

    form_object = UserForm(obj=user_object)
    default_roles = user_object.roles[0]
    return render_template('edit_user.html', def_rol=default_roles, user=user_object, form=form_object)


@app.route('/delete_user/<slug>')
def delete_user(slug):
    user_object = User.query.filter(User.slug==slug)
    return render_template('delete_user.html', user=user_object)

