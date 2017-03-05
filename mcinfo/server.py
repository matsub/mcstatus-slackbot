# coding: utf-8

from japronto import Application, RouteNotFoundException
from .utils import address_match


class InvalidRequest(Exception):
    """This request is not following Slash command format"""
    code = 400


class InvalidToken(Exception):
    """Token doesn't match"""
    code = 400


def error_handler(request, exception):
    code = exception.code
    text = exception.__doc__
    return request.Response(code=code, json={'detail': text})


def not_found(request, exception):
    return request.Response(code=404, text='')


class Server:

    def __init__(self, token, prefix='/'):
        # setting japronto up
        app = Application()
        self.app = app
        self.router = app.router
        self.run = self.app.run

        # server info
        self.token = token
        self.prefix = prefix.rstrip('/')

        # default Error handlers
        self.app.add_error_handler(InvalidRequest, error_handler)
        self.app.add_error_handler(InvalidToken, error_handler)
        self.app.add_error_handler(RouteNotFoundException, not_found)

    def is_acknowledged(self, token):
        return token == self.token

    def route(self, path):
        def _route(f):
            def __route(*args, **kwargs):
                request = args[0]
                command = request.form
                if (command is None) or ('token' not in command):
                    raise InvalidRequest

                token = command['token']
                text = command['text'] if 'text' in command else ''

                address = address_match(text)
                if not self.is_acknowledged(token):
                    raise InvalidToken

                response = f(address)
                return request.Response(text=response)

            # add route
            route = self.prefix, path.lstrip('/')
            route = '/'.join(route)
            self.router.add_route(route, __route)

            return __route
        return _route
