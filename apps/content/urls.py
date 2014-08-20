from django.conf.urls import patterns, url


urlpatterns = patterns(
    'content.views',
    url(r'^files/(?P<filename>.*)$', 'get_file', name='get_file'),
)
