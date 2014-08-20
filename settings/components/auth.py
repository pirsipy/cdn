AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Authentication options
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/signin/'
LOGIN_ERROR_URL = '/signin/failed/'
SESSION_COOKIE_NAME = 'sessionid'

AUTH_USER_MODEL = 'user.User'
