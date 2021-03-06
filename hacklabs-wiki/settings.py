"""
Django settings for our hacklabs-wiki project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import sys

from configurations import Configuration, values


class Common(Configuration):

    ADMINS = (
        ('Admin', 'info@hacklabs-wiki.me'),
    )

    MANAGERS = ADMINS

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(BASE_DIR, 'hacklabs-wiki/apps'))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    TEMPLATE_DEBUG = False

    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.humanize',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'sekizai',
        'sorl.thumbnail',
        'django_nyt',
        'wiki',
        'wiki.plugins.macros',
        'wiki.plugins.help',
        'wiki.plugins.links',
        'wiki.plugins.images',
        'wiki.plugins.attachments',
        'wiki.plugins.notifications',
        'mptt',
    )

    from django import VERSION
    if VERSION < (1, 7):
        INSTALLED_APPS = INSTALLED_APPS + ('south',)
        SOUTH_MIGRATION_MODULES = {
            'django_nyt': 'django_nyt.south_migrations',
            'wiki': 'wiki.south_migrations',
            'images': 'wiki.plugins.images.south_migrations',
            'notifications': 'wiki.plugins.notifications.south_migrations',
            'attachments': 'wiki.plugins.attachments.south_migrations',
        }
    else:
        TEST_RUNNER = 'django.test.runner.DiscoverRunner'

    # Do not user /accounts/profile as default
    #LOGIN_REDIRECT_URL = "/"
    from django.core.urlresolvers import reverse_lazy
    LOGIN_REDIRECT_URL = reverse_lazy('wiki:get', kwargs={'path': ''})
    
    TEMPLATE_CONTEXT_PROCESSORS = Configuration.TEMPLATE_CONTEXT_PROCESSORS + \
        ("django.core.context_processors.request",
         "django.core.context_processors.tz",
         'sekizai.context_processors.sekizai',)

    MIDDLEWARE_CLASSES = (
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )


    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
    )
    
    ROOT_URLCONF = 'hacklabs-wiki.urls'

    WSGI_APPLICATION = 'hacklabs-wiki.wsgi.application'

    DATABASES = values.DatabaseURLValue('sqlite:///{0}'.format(
        os.path.join(BASE_DIR, 'db.sqlite3'),
        environ=True))

    NEVERCACHE_KEY = values.Value('klladsf-wefkjlwef-wekjlwef--wefjlkjfslkxvl')

    #CACHES = values.CacheURLValue('memcached://127.0.0.1:11211')

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'America/New_York'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    SITE_ID = 1

    ALLOWED_HOSTS = values.Value('*')

    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    PROJECT_DIRNAME = BASE_DIR.split(os.sep)[-1]

    CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

    MEDIA_URL = "/media/"

    MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')

    TEMPLATE_DIRS = (os.path.join(BASE_DIR, "hacklabs-wiki/templates"),)
    FIXTURE_DIRS = (os.path.join(BASE_DIR, "fixtures"),)

    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "hacklabs-wiki/static"),
    )

    #DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    AWS_ACCESS_KEY_ID = values.Value()
    AWS_SECRET_ACCESS_KEY = values.Value()
    AWS_STORAGE_BUCKET_NAME = 'example.com'
    AWS_HEADERS = {'ExpiresDefault': 'access plus 30 days',
                   'Cache-Control': 'max-age=86400', }

    # Account activations automatically expire after this period
    ACCOUNT_ACTIVATION_DAYS = 14

    LOGIN_EXEMPT_URLS = ['', '/',
                         '/accounts/login/',
                         'login',
                         '/accounts/signup/']

    LOGIN_URL = '/accounts/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_URL = '/accounts/logout/'

    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

    WIKI_ANONYMOUS_WRITE = True
    WIKI_ANONYMOUS_CREATE = False


class Dev(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = TEMPLATE_DEBUG = True

    DATABASES = values.DatabaseURLValue('sqlite:///{0}'.format(
        os.path.join(Common.BASE_DIR, 'db.sqlite3'),
        environ=True))

    SECRET_KEY = 'notasecretatall'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    INSTALLED_APPS = Common.INSTALLED_APPS + ('debug_toolbar',)

    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',)


class Stage(Common):
    DEBUG = TEMPLATE_DEBUG = True

    SECRET_KEY = values.SecretValue()

    EMAIL_HOST = values.Value('localhost')
    EMAIL_HOST_USER = values.Value()
    EMAIL_HOST_PASSWORD = values.Value()
    EMAIL_PORT = values.Value()
    EMAIL_USE_TLS = values.BooleanValue(False)


class Prod(Common):
    """
    The in-production settings.
    """
    DEBUG = TEMPLATE_DEBUG = False

    SECRET_KEY = values.SecretValue()

    EMAIL_HOST = values.Value('localhost')
    EMAIL_HOST_USER = values.Value()
    EMAIL_HOST_PASSWORD = values.Value()
    EMAIL_PORT = values.Value()
    EMAIL_USE_TLS = values.BooleanValue(False)

    DSN_VALUE = values.Value()

    # If we're on production, connect to Sentry
    #RAVEN_CONFIG = {
    #    'dsn': DSN_VALUE,
    #}

    #INSTALLED_APPS = Common.INSTALLED_APPS + (
    #    'raven.contrib.django.raven_compat',)
