from flask import request, redirect, url_for, render_template, session, jsonify
from flask_login import logout_user

from app import login_manager, User


def search_users():
    if username := dict(request.json).get('username'):
        pass
    user_id = session['_user_id']
    users = [user.serialize for user in (User.query
        .filter(User.username.ilike(username))
        .filter(User.id != user_id).all()
    )]
    print(users)
    return jsonify(users)


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

