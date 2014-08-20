#!/usr/bin/env python
import sys
from concurrent.futures import ThreadPoolExecutor

from tornado import web, wsgi
from tornado.concurrent import run_on_executor
from tornado.web import URLSpec
from tornado.ioloop import IOLoop
from tornado.options import options, define

from wsgi import application as django_app
from django.conf import settings

define('port', type=int, default=8000)
define('host', type=str, default='127.0.0.1')
options.parse_command_line()

APP_SETTINGS = {
    'static_path': settings.STATIC_ROOT,
    'debug': settings.DEBUG,
    'gzip': True}


class ThreadMixin(object):
    executor = ThreadPoolExecutor(max_workers=4)


class FallbackHandler(ThreadMixin, web.FallbackHandler):

    @run_on_executor
    def prepare(self):
        self.fallback(self.request)
        self._finished = True


application = web.Application([
    URLSpec(r'/media/(.*)', web.StaticFileHandler, {'path': settings.MEDIA_ROOT}),
    URLSpec(r'.*', FallbackHandler, {'fallback': wsgi.WSGIContainer(django_app)})], **APP_SETTINGS)


def main():
    if APP_SETTINGS['debug']:
        sys.stdout.write('Host: {}\n'.format(options.host))
        sys.stdout.write('Port: {}\n\n'.format(options.port))
    application.listen(options.port, options.host)
    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        IOLoop.instance().stop()


if __name__ == '__main__':
    main()
