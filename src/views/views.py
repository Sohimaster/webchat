from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, session, redirect, escape, url_for, Response, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from app import *
from src.tables import *
from src.views.forms import *


@login_required
def index():
    return render_template('index.html', username=User.query.get(session['_user_id']).username)


def register():
    if request.method == 'POST':
        pass
    else:
        return render_template('register.html')


def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return render_template('login.html', form=form, errors=form.errors)
            # return '<h1>Invalid form</h1>'
    return render_template('login.html', form=form)


def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)

