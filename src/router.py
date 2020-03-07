from src.views.views import *


class Router:
    @staticmethod
    def apply_routes(app):
        app.add_url_rule('/', 'index', index)
        app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
        app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
        app.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])
        return app
