import random
from pathlib import Path

import factory
from faker import Factory

from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Content
fake = Factory.create()


class ContentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Content

    @factory.lazy_attribute
    def file(self):
        with open(str(random.choice(list(Path('apps/content/test_files').iterdir())).absolute()), 'rb') as f:
            return SimpleUploadedFile('test_filename', f.read())
