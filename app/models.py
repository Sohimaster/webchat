import os

from datetime import datetime
from flask_login import UserMixin

from app import db

USERNAME_LIMIT = 50
EMAIL_LIMIT = 50
PASSWORD_LIMIT = 40
MESSAGE_LIMIT = 1000

CHAT_ICON_NAME_LIMIT = 50
CHAT_NAME_LIMIT = 50


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(USERNAME_LIMIT), unique=True)
    email = db.Column(db.String(EMAIL_LIMIT), unique=True, default=os.urandom(8))
    email_hash = db.Column(db.String(EMAIL_LIMIT), unique=True, nullable=False)
    password = db.Column(db.String(PASSWORD_LIMIT))

    @property
    def serialize(self):
        return {
           'id': self.id,
           'username': self.username,
           'email_hash': self.email_hash
        }


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_member = db.Column(db.Integer, db.ForeignKey('user.id'))
    second_member = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_message = db.Column(db.String(MESSAGE_LIMIT), nullable=True)
    dt_created = db.Column(db.DateTime, default=datetime.now())
    dt_updated = db.Column(db.DateTime, default=datetime.now())

    @property
    def serialize(self):
        return {
           'id': self.id,
           'first_member': self.first_member,
           'second_member': self.second_member,
           'last_message': self.last_message,
           'dt_updated': datetime.strftime(self.dt_updated, '%Y-%m-%d %H:%M:%S')
        }


class ChatMember(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    message = db.Column(db.String(MESSAGE_LIMIT))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dt_created = db.Column(db.DateTime, default=datetime.now())
    dt_updated = db.Column(db.DateTime, default=datetime.now())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'user_id': self.user_id,
            'message': self.message,
            'dt_created': self.dt_created,
            'dt_updated': self.dt_updated
        }
