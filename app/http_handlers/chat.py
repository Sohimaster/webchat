from flask import render_template, session
from flask_login import login_required

from app.models import *
from app.http_handlers.base import BaseHTTPHandler


class ChatHTTPHandler(BaseHTTPHandler):
    @login_required
    def get(self):
        user_id = session['_user_id']
        users = User.query.filter(User.id != user_id).all()
        user_chats = ChatMember.query.get(user_id)
        return render_template('chat.html', users=users)

    @login_required
    def post(self):
        pass
