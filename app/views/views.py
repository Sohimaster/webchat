from flask import request, redirect, url_for, render_template, session, jsonify, Response
from flask_login import logout_user

from app import db, login_manager, User, ChatMember, Chat


def start_chat():
    request_data = request.json
    receiver_id = request_data.get('stranger_id')
    user_id = session['_user_id']
    if receiver_id and user_id and not \
            Chat.query.filter(
                (Chat.first_member.in_((receiver_id, user_id))) &
                (Chat.second_member.in_((receiver_id, user_id))))\
            .first():
        chat = Chat(first_member=receiver_id, second_member=user_id)
        db.session.add(chat)
        db.session.commit()
    return redirect(url_for('chat'))


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
