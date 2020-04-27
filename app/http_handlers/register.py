import hashlib

from flask_login import login_user
from werkzeug.security import generate_password_hash
from flask import render_template, url_for, redirect

from app import app, db
from app.models import User
from app.views.forms import RegisterForm
from app.http_handlers.base import BaseHTTPHandler


class RegisterHTTPHandler(BaseHTTPHandler):
    def get(self, message=None):
        form = RegisterForm()
        return render_template('register.html', form=form, message=message)

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            if not form.repeated_password == form.password:
                return self.get(message='Passwords does not match.')

            password = generate_password_hash(form.password.data)
            if not User.query.filter(User.username == form.username.data).first():
                user = User(username=form.username.data,
                            email=form.email.data,
                            password=password,
                            email_hash=hashlib.sha256(form.email.data.encode('utf-8')).hexdigest())
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('chat'))
            else:
                return self.get(message='User exists.')
        else:
            return self.get(message=f'Please provide a valid {form.errors} value.')
