from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app import db
from werkzeug.urls import url_parse
from datetime import datetime

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('show_main_page'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data
        
        user = User(username=username, email=email, password_hash=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        # Make flash message
        flash(f'Account created for {user.username}', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=reg_form)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.show_main_page'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        remember = login_form.remember.data

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash(f'Welcome back {user.username}', 'info')
            login_user(user, remember=remember)
            next_url = request.args.get('next')
            
            if not next_url or url_parse(next_url).netloc != '':
                next_url = url_for('main.show_main_page')
            return redirect(next_url)

        else:
            flash(f'Incorrect email or password', 'warning')
        
    return render_template('auth/login.html', form=login_form)


@auth.route('/logout/')
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('main.show_main_page'))