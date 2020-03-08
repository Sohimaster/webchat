from flask_login import login_user
from werkzeug.security import check_password_hash
from flask import render_template, url_for, redirect

from app import *
from app.models import *
from app.views.forms import LoginForm
from app.http_handlers.base import BaseHTTPHandler


class LoginHTTPHandler(BaseHTTPHandler):
    def get(self, message=None):
        form = LoginForm()
        return render_template('login.html', form=form, message=message)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('chat'))
        return self.get(message='Wrong username or password!')
