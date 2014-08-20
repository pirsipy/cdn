from uuid import uuid4
import gridfs
import magic

from mongoengine.django.storage import GridFSStorage
from pymongo import MongoClient

from django.conf import settings

from core.utils import reverse

db = MongoClient()[settings.MONGODB_NAME]
fs = gridfs.GridFS(db)


class Storage(GridFSStorage):

    def get_available_name(self, name):
        return '.'.join([uuid4().hex, name.lower().split('.')[-1]])

    def url(self, name):
        return reverse('content:file', kwargs={'filename': name})

    def _save(self, name, content):
        doc = self.document()
        content_type = magic.from_buffer(content.read(1024), mime=True).decode('utf-8')
        content.seek(0)
        getattr(doc, self.field).put(content, filename=name, content_type=content_type)
        doc.save()
        return name
