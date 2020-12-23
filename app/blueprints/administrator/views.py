from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from app.models import User, Post
from flask_login import login_required, current_user
from functools import wraps
from app.forms import AdminUserUpdateForm, AdminUserCreateForm
from app import db

administrator = Blueprint('administrator', __name__, template_folder='templates')

def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwags):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwags)
    return decorated_view


@administrator.route('/administrator/')
@login_required
@admin_login_required
def home_admin():
    return render_template('administrator/admin_home.html')


@administrator.route('/administrator/users/')
@login_required
@admin_login_required
def users_list_admin():
    users = User.query.all()
    return render_template('administrator/admin_users_list.html', users=users)


@administrator.route('/administrator/users/create/', methods=['POST', 'GET'])
@login_required
@admin_login_required
def user_create_admin():
    form = AdminUserCreateForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        admin = form.admin.data
        user = User(username=username, email=email, password_hash=password, admin=admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash(f'User {user.username} has been successfully created!', 'success')
        return redirect(url_for('administrator.home_admin'))

    return render_template('administrator/admin_create_user.html', form=form)


@administrator.route('/administrator/users/<int:user_id>/update/', methods=['POST', 'GET'])
@login_required
@admin_login_required
def user_update_admin(user_id):
    user = User.query.get(user_id)
    form = AdminUserUpdateForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.admin.data is None:
            user.admin = False
        else:
            user.admin = form.admin.data
        
        db.session.commit()
        flash(f'User {user.username} has been successfully updated', 'success')
        return redirect(url_for('administrator.home_admin'))

    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.admin.data = user.admin
    return render_template('administrator/admin_update_user.html', form=form, user=user)


@administrator.route('/administrator/users/<int:user_id>/delete/', methods=['GET'])
@login_required
@admin_login_required
def user_delete_admin(user_id):
    user = User.query.get(user_id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'User {username} has been successfully deleted!', 'success')
    return redirect(url_for('administrator.home_admin'))