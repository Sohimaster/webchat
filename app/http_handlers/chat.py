from flask import render_template, session
from flask_login import login_required

from app.models import *
from app.http_handlers.base import BaseHTTPHandler


class ChatHTTPHandler(BaseHTTPHandler):
    @login_required
    def get(self):
        users = []
        user_id = int(session['_user_id'])
        user_chats = Chat.query.filter(
            (Chat.first_member == user_id) | (Chat.second_member == user_id)
        ).all()
        user_chats_serialized = [user_chat.serialize for user_chat in user_chats]
        if user_chats_serialized:
            user_ids = [user_chat['first_member']
                        if user_chat['first_member'] != user_id else user_chat['second_member']
                        for user_chat in user_chats_serialized]
            users = User.query.filter(User.id.in_(user_ids)).all()
        return render_template('chat.html', users=users)

    @login_required
    def post(self):
        pass
