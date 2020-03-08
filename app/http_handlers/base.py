from flask.views import MethodView
from abc import abstractmethod


class BaseHTTPHandler(MethodView):

    @abstractmethod
    def get(self):
        raise NotImplementedError()

    @abstractmethod
    def post(self):
        raise NotImplementedError()
