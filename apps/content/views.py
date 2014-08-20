import json

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http.response import HttpResponse

from .models import Content
from .storage import fs


class FileView(View):

    def get(self, request, filename, *args, **kwargs):
        f = fs.get_last_version(filename=filename)
        return HttpResponse(f.read(), content_type=f.content_type)

    def post(self, request, filename=None, *args, **kwargs):
        data = {}
        for f in request.FILES.getlist('file'):
            content = Content.objects.create(file=f)
            data[f.name] = content.get_absolute_url()
        return HttpResponse(json.dumps(data), content_type='application/json')


get_file = csrf_exempt(FileView.as_view())
