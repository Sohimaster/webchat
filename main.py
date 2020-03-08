from app import app
from app.router import Router


app = Router.apply_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9191)
