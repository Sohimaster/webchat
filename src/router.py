from src.views.views import *


class Router:
    @staticmethod
    def apply_routes(app):
        app.add_url_rule('/', 'index', index)
        app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
        app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
        app.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])

        # app.add_url_rule('/automatching',
        #                  'automatching',
        #                  view_func=AutoMatcher.as_view('automatcher'))
        # app.add_url_rule('/filematching',
        #                  'filematching',
        #                  view_func=FileMatcher.as_view('filematcher'))
        # app.add_url_rule('/clients',
        #                  'clients',
        #                  view_func=Client.as_view('clients'))
        # app.add_url_rule('/products',
        #                  'products',
        #                  view_func=Product.as_view('products'))
        # app.add_url_rule('/matching',
        #                  'matching',
        #                  view_func=Matching.as_view('matching'))
        #
        # app.add_url_rule('/csv', 'csv', send_csv, methods=['GET'])
        return app
