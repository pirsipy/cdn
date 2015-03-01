import os
from mimetypes import guess_type
from pathlib import Path
from uuid import uuid4

from pulsar.apps import wsgi
from pulsar.apps.wsgi import Json

BASE_PATH = '/home/webmaster/app/files'


class Router(wsgi.Router):

    def get_destination_dir(self, _hex):
        path = Path().joinpath(_hex[:2], _hex[2:4], _hex[4:6])
        path = path.joinpath(BASE_PATH, path)
        try:
            path.mkdir(parents=True)
        except FileExistsError:
            pass
        return path

    def get_filename(self, source_name, _hex):
        name = _hex[22:]
        _, ext = os.path.splitext(source_name)
        name += ext
        return name

    def get_url(self, proto, origin_host, destination):
        host, port = origin_host.split(':')
        host = origin_host if port not in ['80', '443'] else host
        return '{0}://{1}{2}'.format(proto, host, str(destination).replace(BASE_PATH, ''))

    def post(self, request):
        self.data = request.data_and_files()[0]
        host = request.get_host()
        proto = request.uri.split(':', 1)[0]
        name_list = self.data.getlist('name')
        path_list = self.data.getlist('path')
        size_list = self.data.getlist('size')
        md5_list = self.data.getlist('md5')
        response = []
        for name, path, size, md5 in zip(name_list, path_list, size_list, md5_list):
            _hex = uuid4().hex
            destination_dir = self.get_destination_dir(_hex)
            filename = self.get_filename(name, _hex)

            source = Path(path)
            destination = destination_dir.joinpath(filename)

            source.rename(destination)
            url = self.get_url(proto, host, destination)
            content_type = guess_type(url)[0] or ''
            response.append({
                'url': url, 'type': content_type, 'name': name,
                'size': size, 'md5': md5})
        return Json(response).http_response(request)


class Site(wsgi.LazyWsgi):

    def setup(self, environ):
        return wsgi.WsgiHandler([Router('/upload/')])


def server():
    return wsgi.WSGIServer(Site(), description='Upload handler')


if __name__ == '__main__':
    server().start()
