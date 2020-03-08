from app.views import *
from app.sockets import *
from app.http_handlers import *


class Router:
    @staticmethod
    def apply_routes(app):
        app.add_url_rule('/', 'index', lambda: redirect(url_for('chat')))
        app.add_url_rule('/chat', 'chat', view_func=Chat.as_view('chat'))
        app.add_url_rule('/login', 'login', view_func=Login.as_view('login'))
        app.add_url_rule('/register', 'register', view_func=Register.as_view('register'))
        app.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])
        return app

    @staticmethod
    def apply_socketio_routes(sio):
        sio.on_event('message', send_message)
        sio.on_event('join_chat', join_chat)
        sio.on_event('leave_chat', leave_chat)
