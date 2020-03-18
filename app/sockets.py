from flask import session
from dataclasses import dataclass
from flask_socketio import emit, join_room, leave_room


@dataclass
class Message:
    sender_id: int
    receiver_id: int
    datetime: str
    message: str

    @property
    def serialize(self):
        return {
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'datetime': self.datetime,
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


def on_message(datetime, message, receiver_id):
    message_data = Message(datetime=datetime, sender_id=session.get('_user_id'), receiver_id=receiver_id, message=message)
    emit('render_message', message_data.serialize)
