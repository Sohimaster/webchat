import json

from flask import session
from flask.json import JSONEncoder
from datetime import datetime
from dataclasses import dataclass
from flask_socketio import emit, join_room, leave_room

from app import db
from app.models import Message, Chat, User


@dataclass
class SocketMessage:
    sender_id: int
    receiver_id: int
    datetime: datetime
    message: str

    @property
    def serialize(self):
        return {
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'datetime': json.dumps(self.datetime, cls=JSONEncoder),
            'message': self.message
        }


def on_join(data):
    username = data.get('user_name', '')
    room = data.get('room', '')
    join_room(room)
    emit(username + ' has entered the room.', room=room)


def on_leave(data):
    username = data.get('user_name')
    room = data.get('room')
    leave_room(room)
    emit(username + ' has left the room.', room=room)


def on_message(_datetime, message, receiver_id):
    message_data = SocketMessage(
        datetime=datetime.strptime(_datetime, '%Y-%m-%d %H:%M:%S'),
        sender_id=session.get('_user_id'),
        receiver_id=receiver_id,
        message=message)
    chat_id = Chat.query.filter(
        (Chat.first_member.in_((message_data.receiver_id, message_data.sender_id))) &
        (Chat.second_member.in_((message_data.receiver_id, message_data.sender_id)))
    ).first().id

    new_message = Message(
        message=message_data.message,
        chat_id=chat_id,
        user_id=message_data.sender_id,
        dt_created=message_data.datetime,
        dt_updated=message_data.datetime
    )
    db.session.add(new_message)
    db.session.commit()
    emit('render_message', message_data.serialize)
