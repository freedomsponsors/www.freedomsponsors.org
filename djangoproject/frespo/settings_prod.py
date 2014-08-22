from settings import *
import os

ALLOWED_HOSTS = ['freedomsponsors.org', 'www.freedomsponsors.org']
ADMINS = (
    ('Tony', 'tonylampada@gmail.com'),
    ('Kang', 'zhaokang.cn@gmail.com'),
)
MANAGERS = ADMINS
SECRET_KEY = os.environ['SECRET_KEY']

ENABLE_PIWIK = True

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_PROTOCOL = 'https'
SITE_HOST = 'freedomsponsors.org'
SITE_NAME = 'FreedomSponsors'
SITE_HOME = SITE_PROTOCOL+'://'+SITE_HOST

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#--------- Use Gmail
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#--------- Use a local postfix
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False

MEDIA_ROOT = '/home/frespo/media'
MEDIA_ROOT_URL = '/media'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'frespo',
        'USER': 'frespo',
        'PASSWORD': os.environ['PG_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

MIDDLEWARE_CLASSES = (
    'core.middlewares.ErrorMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middlewares.FSPreconditionsMiddleware',
    'core.middlewares.Translation',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': 'unix:/tmp/memcache.socket',
#        'TIMEOUT': 2,
#    }
#}
#CACHE_MIDDLEWARE_SECONDS = 15
#CACHE_MIDDLEWARE_ALIAS = 'default'

GITHUB_BOT_USERNAME = 'freedomsponsors-bot'
GITHUB_BOT_PASSWORD = os.environ['GITHUB_BOT_PASSWORD']

SERVER_EMAIL = 'errors@freedomsponsors.org'
DEFAULT_FROM_EMAIL = 'noreply@freedomsponsors.org'
ADMAIL_FROM_EMAIL = 'tony@freedomsponsors.org'

PAYPAL_USE_SANDBOX = False
PAYPAL_IPNNOTIFY_URL_TOKEN = os.environ['PAYPAL_IPNNOTIFY_URL_TOKEN']
PAYPAL_IPNNOTIFY_URL = 'https://freedomsponsors.org/core/paypal/'+PAYPAL_IPNNOTIFY_URL_TOKEN
BITCOIN_IPNNOTIFY_URL_TOKEN = os.environ['BITCOIN_IPNNOTIFY_URL_TOKEN']
BITCOIN_ENABLED = True

OPENEXCHANGERATES_API_KEY = os.environ['OPENEXCHANGERATES_API_KEY']
MOCK_OPENEXCHANGE_RATES = False

BITCOINRPC_CONN = {
    'remote': True,
    'user': os.environ['BITCOINRPC_CONN_USER'],
    'password': os.environ['BITCOINRPC_CONN_PASSWORD'],
    'host': os.environ['BITCOINRPC_CONN_HOST'],
    'port': 443,
    'use_https': True
}

PAYPAL_API_USERNAME          = os.environ['PAYPAL_API_USERNAME']
PAYPAL_API_PASSWORD          = os.environ['PAYPAL_API_PASSWORD']
PAYPAL_API_SIGNATURE         = os.environ['PAYPAL_API_SIGNATURE']
PAYPAL_API_APPLICATION_ID    = os.environ['PAYPAL_API_APPLICATION_ID']
PAYPAL_API_EMAIL             = os.environ['PAYPAL_API_EMAIL']
PAYPAL_FRESPO_RECEIVER_EMAIL = os.environ['PAYPAL_FRESPO_RECEIVER_EMAIL']

TWITTER_CONSUMER_KEY         = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET      = os.environ['TWITTER_CONSUMER_SECRET']
FACEBOOK_APP_ID              = os.environ['FACEBOOK_APP_ID']
FACEBOOK_API_SECRET          = os.environ['FACEBOOK_API_SECRET']
GITHUB_APP_ID                = os.environ['GITHUB_APP_ID']
GITHUB_API_SECRET            = os.environ['GITHUB_API_SECRET']
BITBUCKET_CONSUMER_KEY       = os.environ['BITBUCKET_CONSUMER_KEY']
BITBUCKET_CONSUMER_SECRET    = os.environ['BITBUCKET_CONSUMER_SECRET']

os.environ.setdefault('FRESPO_LOG_FILE', 'frespo.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
#            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/home/frespo/logs/%s' % os.environ['FRESPO_LOG_FILE'],
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'core.management.commands.bitcoin_jobs': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['null'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
