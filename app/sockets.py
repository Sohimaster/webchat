import json

from flask import session
from flask.json import JSONEncoder
from datetime import datetime
from dataclasses import dataclass
from flask_socketio import join_room, leave_room

from app import db, sio
from app.models import Message, Chat, User


@dataclass
class SocketMessage:
    sender_id: int
    chat_id: int
    datetime: datetime
    message: str

    @property
    def serialize(self):
        return {
            'sender_id': self.sender_id,
            'chat_id': self.chat_id,
            'datetime': json.dumps(self.datetime, cls=JSONEncoder),
            'message': self.message
        }


def on_join(chat_id):
    user_id = int(session.get('_user_id'))
    chat = Chat.query.get(chat_id)
    if chat.first_member == user_id or chat.second_member == user_id:
        join_room(chat_id)


def on_leave(data):
    username = data.get('user_name')
    room = data.get('room')
    leave_room(room)
    sio.emit(username + ' has left the room.', room=room)


def on_message(_datetime, message, chat_id):
    message_data = SocketMessage(
        datetime=datetime.strptime(_datetime, '%Y-%m-%d %H:%M:%S'),
        sender_id=session.get('_user_id'),
        chat_id=chat_id,
        message=message)
    chat = Chat.query.get(chat_id)
    chat.last_message = message_data.message
    chat.dt_updated = message_data.datetime

    new_message = Message(
        message=message_data.message,
        chat_id=chat.id,
        user_id=message_data.sender_id,
        dt_created=message_data.datetime,
        dt_updated=message_data.datetime
    )
    db.session.add(new_message)
    db.session.commit()
    sio.emit('render_message', message_data.serialize)
