from flask import request, redirect, url_for, render_template, session, jsonify
from flask_login import logout_user

from app import login_manager, User


def search_users():
    username = request.json.get('username')
    user_id = session['_user_id']
    users = [user.serialize for user in
             (User.query
              .filter(User.username.ilike(username))
              .filter(User.id != user_id).all())]
    return jsonify(users)


def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)
