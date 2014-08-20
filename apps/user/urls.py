from django.conf.urls import patterns, url

urlpatterns = patterns(
    'user.views',
    url(r'^$', 'user_detail', name='detail'),
)
