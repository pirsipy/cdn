PROJECT_NAME = 'cdn'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DOMAIN = 'cdn.com'
ALLOWED_HOSTS = [DOMAIN]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SECRET_KEY = '10$g&amp;#uzn7=xg3*nux6pt%(ts_@$f!rh!^-bnsve*vpa6y7_nq'
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
DEFAULT_FILE_STORAGE = 'content.storage.Storage'
FILE_UPLOAD_MAX_MEMORY_SIZE = 50
