from flask_login import login_required
from flask import render_template, session, \
    request, redirect, url_for

from app.models import *
from app.http_handlers.base import BaseHTTPHandler


class ChatHTTPHandler(BaseHTTPHandler):
    @login_required
    def get(self):
        user_id = int(session['_user_id'])

        receiver_ids = []
        mapped_chat_id_with_users = {}

        user_chats = Chat.query.filter(
            (Chat.first_member == user_id) | (Chat.second_member == user_id)
        ).all()
        user_chats_serialized = [user_chat.serialize for user_chat in user_chats]

        for chat in user_chats_serialized:
            chat_messages = Message.query.filter(Message.chat_id == chat['id']).all()
            chat_messages_serialized = [chat_message.serialize for chat_message in chat_messages]

            chat_messages_sorted = sorted(
                chat_messages_serialized, key=lambda x: x.get('dt_created'))
            chat['messages'] = chat_messages_sorted

            receiver_id = chat['first_member'] if chat['first_member'] != user_id \
                else chat['second_member']
            receiver_ids.append(receiver_id)
            mapped_chat_id_with_users[chat['id']] = User.query.filter(User.id == receiver_id).first()

        user_chats = sorted(user_chats_serialized, key=lambda x: x.get('dt_updated'), reverse=True)
        return render_template('chat.html', chats=user_chats, mapped=mapped_chat_id_with_users)

    @login_required
    def post(self):
        request_data = request.json
        receiver_id = request_data.get('stranger_id')
        user_id = session['_user_id']
        if receiver_id and user_id and not \
                Chat.query.filter(
                    (Chat.first_member.in_((receiver_id, user_id))) &
                    (Chat.second_member.in_((receiver_id, user_id)))) \
                        .first():
            chat = Chat(first_member=receiver_id, second_member=user_id)
            db.session.add(chat)
            db.session.commit()
        return redirect(url_for('chat'))