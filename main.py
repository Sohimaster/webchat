from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room


app = Flask(__name__)
app.secret_key = b'\xa8\x12\xd1\x026\x14cr\x83\xb6\xcdL\xe5\xf7dA'
sio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@sio.on('join')
def on_join(data):
    username = data.get('user_name', '')
    room = data.get('room', '')
    join_room(room)
    sio.emit(username + ' has entered the room.', room=room)


@sio.on('leave')
def on_leave(data):
    username = data.get('user_name')
    room = data.get('room')
    leave_room(room)
    sio.emit(username + ' has left the room.', room=room)


@sio.on('message')
def handle_message(json):
    print('msg: ', str(json))
    on_join(json)
    sio.emit('response', json, room=json.get('room', ''))


if __name__ == '__main__':
    sio.run(app, debug=True, host='0.0.0.0')