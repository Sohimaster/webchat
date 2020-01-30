from flask import Flask, render_template, \
    request, session, redirect, escape, url_for, Response
from flask_socketio import SocketIO, join_room, leave_room


app = Flask(__name__)
app.secret_key = b'\xa8\x12\xd1\x026\x14cr\x83\xb6\xcdL\xe5\xf7dA'
sio = SocketIO(app)


# @app.route('/')
# def index():
#     return render_template('index.html')


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


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if username := request.form.get('username'):
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/test')
def test():
    print(session)
    return Response([])


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    sio.run(app, debug=True, host='0.0.0.0')
