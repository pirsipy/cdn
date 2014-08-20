#!/usr/bin/env python
from pulsar.apps.wsgi import WSGIServer, LazyWsgi, WsgiHandler, wait_for_body_middleware

from wsgi import application


class Wsgi(LazyWsgi):

    def setup(self, environ=None):
        return WsgiHandler((wait_for_body_middleware, application))


if __name__ == '__main__':
    callable = Wsgi()
    callable.setup()
    WSGIServer(callable=callable, name='cdn').start()
