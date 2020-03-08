import os
import time

from flask_login import UserMixin

from app import db

USERNAME_LIMIT = 50
EMAIL_LIMIT = 50
PASSWORD_LIMIT = 40
MESSAGE_LIMIT = 1000

CHAT_ICON_NAME_LIMIT = 50
CHAT_NAME_LIMIT = 50


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_LIMIT), unique=True)
    email = db.Column(db.String(EMAIL_LIMIT), unique=True, default=os.urandom(8))
    email_hash = db.Column(db.String(EMAIL_LIMIT), unique=True, nullable=False)
    password = db.Column(db.String(PASSWORD_LIMIT))


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(CHAT_NAME_LIMIT))
    image = db.Column(db.String(CHAT_ICON_NAME_LIMIT))
    last_message = db.Column(db.String(MESSAGE_LIMIT))
    dt_created = db.Column(db.DateTime, default=time.time())
    dt_updated = db.Column(db.DateTime, default=time.time())


class ChatMember(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    message = db.Column(db.String(MESSAGE_LIMIT))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dt_created = db.Column(db.DateTime, default=time.time())
    dt_updated = db.Column(db.DateTime, default=time.time())


