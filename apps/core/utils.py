from django.conf import settings
from django.core.urlresolvers import reverse as django_reverse


def reverse(*args, **kwargs):
    return 'http://%s%s' % (settings.DOMAIN, django_reverse(*args, **kwargs))
