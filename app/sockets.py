from flask_socketio import emit, join_room, leave_room


def join_chat(data):
    username = data.get('user_name', '')
    room = data.get('room', '')
    join_room(room)
    emit(username + ' has entered the room.', room=room)


def leave_chat(data):
    username = data.get('user_name')
    room = data.get('room')
    leave_room(room)
    emit(username + ' has left the room.', room=room)


def send_message(json):
    print('msg: ', str(json))
    emit('response', json, room=json.get('room', ''))