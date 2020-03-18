from app import app, sio
from app.router import Router


app = Router.apply_routes(app)
sio = Router.apply_socketio_routes(sio)
if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=9191)
