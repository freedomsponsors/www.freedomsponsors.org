# coding: utf-8
from decimal import Decimal
from unipath import Path
import os

PROJECT_DIR = Path(__file__).parent.parent
SECRET_KEY = '*bz++cf(*#++vpo+b+=m3%p9#*x$$&amp;0mjs90x3oo5u@^zyvh)0'

FRESPO_PROJECT_ID = -1 # only needed for backwards compatibility with south patch 0008_set_isfeedback_true.py


MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT', PROJECT_DIR.child('core').child('static').child('media'))
MEDIA_ROOT_URL = '/media'

SITE_NAME = 'FreedomSponsors'
SITE_PROTOCOL = os.getenv('DJANGO_SITE_PROTOCOL', 'http')
SITE_HOST = os.getenv('DJANGO_SITE_HOST', 'localhost:8000')
SITE_HOME = SITE_PROTOCOL+'://'+SITE_HOST

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = ''
STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', '')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MIDDLEWARE_CLASSES = (
    'core.middlewares.ErrorMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middlewares.FSPreconditionsMiddleware',
    'core.middlewares.Translation',
    # 'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',  # tava aih so no settings de dev
    'django.middleware.cache.FetchFromCacheMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR.child("templates"),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

ROOT_URLCONF = 'frespo.urls'

WSGI_APPLICATION = 'frespo.wsgi.application'

LOCALE_PATHS = (
    PROJECT_DIR.child("locale"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'bitcoin_frespo',
    'frespo_currencies',
    'statfiles',
    'core',
    # 'sandbox',
    'gh_frespo_integration',
    # 'bootstrap-pagination'
    # 'social-auth-app-django',
    # 'social.apps.django_app.default',
    'social_django',
    # 'south',
    'emailmgr',
    'registration',
    'captcha',
)


RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = False
RECAPTCHA_USE_SSL = True


AUTHENTICATION_BACKENDS = (
    # 'social.backends.google.GoogleOpenIdConnect',
    # 'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google_openidconnect.GoogleOpenIdConnect',
    # 'social.backends.github.GithubOAuth2',
    'social_core.backends.github.GithubOAuth2',
    # 'social.backends.facebook.FacebookOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # 'social.backends.bitbucket.BitbucketOAuth',
    'social_core.backends.bitbucket.BitbucketOAuth',
    # 'social.backends.twitter.TwitterOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    # 'social.backends.open_id.OpenIdAuth',
    'social_core.backends.open_id.OpenIdAuth',
    # 'social.backends.yahoo.YahooOpenId',
    'social_core.backends.yahoo.YahooOpenId',

    'django.contrib.auth.backends.ModelBackend',
)

SOCIALAUTH_PIPELINE_TRUSTED_BACKENDS = [
    'social.backends.google.GoogleOpenIdConnect',
    'social.backends.github.GithubOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.bitbucket.BitbucketOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.yahoo.YahooOpenId',
]

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'frespo.socialauth_pipeline.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

TEST_GMAIL_ACCOUNT_1 = {
    'username' : 'eunemqueriaessacontamesmo',
    'password' : 'blimblom',
}
TEST_GMAIL_ACCOUNT_2 = {
    'username' : 'minhaoutracontafake',
    'password' : 'blimblom',
}


SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email',]
#GITHUB_EXTENDED_PERMISSIONS = ['public_repo']
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email',]


LOGIN_URL          = '/login'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_GITHUB_SCOPE = ['login', 'social_username']
SOCIAL_AUTH_GITHUB_EXTRA_DATA = [('login', 'social_username')]
FACEBOOK_EXTRA_DATA = [('username', 'social_username')]
TWITTER_EXTRA_DATA = [('screen_name', 'social_username')]

SOCIAL_AUTH_TWITTER_KEY                 = os.getenv('TWITTER_CONSUMER_KEY')
SOCIAL_AUTH_TWITTER_SECRET              = os.getenv('TWITTER_CONSUMER_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY                = os.getenv('FACEBOOK_APP_ID')
SOCIAL_AUTH_FACEBOOK_SECRET             = os.getenv('FACEBOOK_API_SECRET')
SOCIAL_AUTH_GITHUB_KEY                  = os.getenv('GITHUB_APP_ID')
SOCIAL_AUTH_GITHUB_SECRET               = os.getenv('GITHUB_API_SECRET')
SOCIAL_AUTH_BITBUCKET_KEY               = os.getenv('BITBUCKET_CONSUMER_KEY')
SOCIAL_AUTH_BITBUCKET_SECRET            = os.getenv('BITBUCKET_CONSUMER_SECRET')
SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_KEY    = os.getenv('SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_KEY')
SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_SECRET')

ACCOUNT_ACTIVATION_DAYS = 1

LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_INACTIVE_USER_MESSAGE = 'This account has been deactivated'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

PAGINATION_DEFAULT_PAGINATION = 10
PAGINATION_DEFAULT_ORPHANS = 5

##############################################################
# settings that are likely to change on different environments
# ############################################################

ALLOWED_HOSTS = ['freedomsponsors.org', 'www.freedomsponsors.org', 'test.freedomsponsors.org', 'localhost']
ADMINS = (
    ('Tony', 'tonylampada@gmail.com'),
    ('Hugo', 'hugodieb.hd@gmail.com'),
)
MANAGERS = ADMINS
ADMAIL_FROM_EMAIL = 'tony@freedomsponsors.org'


DEBUG = os.getenv('DJANGO_DEBUG', '1') == '1'
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = os.getenv('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend') # 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(os.getenv('DJANGO_EMAIL_PORT', '25'))
EMAIL_USE_TLS = os.getenv('DJANGO_EMAIL_USE_TLS', '0') == '1'
DEFAULT_FROM_EMAIL = 'noreply@freedomsponsors.org'



SKIPTESTS_TRACKERINTEGRATION = False # Skip tests in tests_trackerintegration
SKIPTESTS_BITCOINADAPTER = True
SKIPTESTS_PAYPALAPI = True
SKIPTESTS_ACCOUNTGMAIL = True

FS_FEE = Decimal('0.03')
BITCOIN_FEE = Decimal('0.0002')
FETCH_ISSUE_TIMEOUT = 10.0
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '*bz++cf(*#++vpo+b+=m3%p9#*x$$&amp;0mjs90x3oo5u@^zyvh)0')
ENABLE_PIWIK = os.getenv('ENABLE_PIWIK', '0') == '1'

GITHUB_BOT_USERNAME = 'freedomsponsors-bot'
GITHUB_BOT_PASSWORD = os.getenv('GITHUB_BOT_PASSWORD', '*********')

PAYPAL_USE_SANDBOX           = os.getenv('PAYPAL_USE_SANDBOX', '1') == '1'
PAYPAL_DEBUG                 = os.getenv('PAYPAL_DEBUG', '0') == '1'
PAYPAL_IPNNOTIFY_URL_TOKEN   = os.getenv('PAYPAL_IPNNOTIFY_URL_TOKEN', 'megablasteripn')
PAYPAL_API_USERNAME          = os.getenv('PAYPAL_API_USERNAME', "FP_1338073142_biz_api1.gmail.com")
PAYPAL_API_PASSWORD          = os.getenv('PAYPAL_API_PASSWORD', '1338073168')
PAYPAL_API_SIGNATURE         = os.getenv('PAYPAL_API_SIGNATURE', 'AFcWxV21C7fd0v3bYYYRCpSSRl31AVAvZTYca4potYVRXAbpeSKQGHZO')
PAYPAL_API_APPLICATION_ID    = os.getenv('PAYPAL_API_APPLICATION_ID', 'APP-80W284485P519543T')  #see www.x.com
PAYPAL_API_EMAIL             = os.getenv('PAYPAL_API_EMAIL', 'FP_1338073142_biz@gmail.com')
PAYPAL_FRESPO_RECEIVER_EMAIL = os.getenv('PAYPAL_FRESPO_RECEIVER_EMAIL', 'FP_1338073142_biz@gmail.com')

PAYPAL_CANCEL_URL = SITE_HOME+'/core/paypal/cancel'
PAYPAL_RETURN_URL = SITE_HOME+'/core/paypal/return'
PAYPAL_IPNNOTIFY_URL = SITE_HOME+'/core/paypal/'+PAYPAL_IPNNOTIFY_URL_TOKEN


BITCOIN_ENABLED = os.getenv('BITCOIN_ENABLED', '0') == '1'
BITCOIN_IPNNOTIFY_URL_TOKEN = os.getenv('BITCOIN_IPNNOTIFY_URL_TOKEN', 'megablasteripn')
BITCOIN_RECEIVE_ADDRESS_POOL_SIZE = 20
BITCOINRPC_CONN = {
    'remote': os.getenv('BITCOINRPC_CONN_REMOTE') == '1',
    'user': os.getenv('BITCOINRPC_CONN_USER'),
    'password': os.getenv('BITCOINRPC_CONN_PASSWORD'),
    'password2': os.getenv('BITCOINRPC_CONN_PASSWORD2'),
    'host': os.getenv('BITCOINRPC_CONN_HOST'),
    'port': int(os.getenv('BITCOINRPC_CONN_PORT', '443')),
    'use_https': os.getenv('BITCOINRPC_CONN_USE_HTTPS') == '1',
}


MOCK_OPENEXCHANGE_RATES = os.getenv('MOCK_OPENEXCHANGE_RATES', '1') == '1'
OPENEXCHANGERATES_API_KEY = os.getenv('OPENEXCHANGERATES_API_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ATOMIC_REQUESTS': True,
        'NAME': os.getenv('DATABASE_NAME', 'frespo'),
        'USER': os.getenv('DATABASE_USER', 'frespo'),
        'PASSWORD': os.getenv('DATABASE_PASS', 'frespo'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

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
            'class':'logging.NullHandler',
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
            'filename': os.getenv('FRESPO_LOG_FILE', PROJECT_DIR.child('logs', 'frespo.log')),
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
