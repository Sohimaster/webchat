from flask import request, redirect, url_for, session, jsonify
from flask_login import logout_user, login_required

from app import login_manager, User


@login_required
def search_users():
    username = request.json.get('username')
    user_id = session['_user_id']
    users = [user.serialize for user in
             (User.query
              .filter(User.username.contains(username))
              .filter(User.id != user_id).all())]
    return jsonify(users)


def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)
