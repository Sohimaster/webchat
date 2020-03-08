from flask import render_template, session
from flask_login import login_required

from app.models import *
from app.http_handlers.base import BaseHTTPHandler


class MessageHTTPHandler(BaseHTTPHandler):
    @login_required
    def get(self):
        pass

    @login_required
    def post(self):
        pass
