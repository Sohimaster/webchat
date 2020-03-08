from flask import request, redirect, url_for, render_template
from flask_login import logout_user

from app import login_manager, User


def register():
    if request.method == 'POST':
        pass
    else:
        return render_template('register.html')


def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)

