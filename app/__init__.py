import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

TEMPLATE_DIR = os.path.abspath('src/views/templates')
STATIC_DIR = os.path.abspath('src/views/static')

app = Flask('webchat', template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'test_key'  # os.urandom(32)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

