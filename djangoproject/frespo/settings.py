# Django settings for frespo project.
import os
from decimal import Decimal
import sys
import env_settings

FS_FEE = Decimal('0.03')


DEBUG = env_settings.DEBUG
FRESPO_PROJECT_ID = env_settings.FRESPO_PROJECT_ID # Feedback issues
TEST_GMAIL_ACCOUNT_1 = env_settings.TEST_GMAIL_ACCOUNT_1
TEST_GMAIL_ACCOUNT_2 = env_settings.TEST_GMAIL_ACCOUNT_2
ADMINS = env_settings.ADMINS
DATABASE_NAME = env_settings.DATABASE_NAME
DATABASE_USER = env_settings.DATABASE_USER
DATABASE_PASS = env_settings.DATABASE_PASS

TEMPLATE_DEBUG = DEBUG
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DATABASE_NAME,                      # Or path to database file if using sqlite3.
        'USER': DATABASE_USER,                      # Not used with sqlite3.
        'PASSWORD': DATABASE_PASS,                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# if 'test' in sys.argv:
#     DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

fakeEmails = True
if(fakeEmails):
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    MAILER_EMAIL_BACKEND = EMAIL_BACKEND
    EMAIL_FILE_PATH = './fakeMail'
else:
#    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = env_settings.AUTO_EMAIL_USERNAME
    EMAIL_HOST_PASSWORD = env_settings.AUTO_EMAIL_PASSWORD
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = env_settings.AUTO_EMAIL_USERNAME

SITE_PROTOCOL = 'http'
SITE_HOST = env_settings.SITE_HOST
SITE_NAME = env_settings.SITE_NAME
SITE_HOME = SITE_PROTOCOL+'://'+SITE_HOST

PAYPAL_CANCEL_URL = SITE_HOME+'/core/paypal/cancel'
PAYPAL_RETURN_URL = SITE_HOME+'/core/paypal/return'
PAYPAL_IPNNOTIFY_URL = SITE_HOME+'/core/paypal/megablasteripn'

PAYPAL_USE_SANDBOX = env_settings.PAYPAL_USE_SANDBOX
PAYPAL_DEBUG = False
if(PAYPAL_USE_SANDBOX):
    PAYPAL_API_USERNAME = env_settings.PAYPAL_SANDBOX_API_USERNAME
    PAYPAL_API_PASSWORD = env_settings.PAYPAL_SANDBOX_API_PASSWORD
    PAYPAL_API_SIGNATURE = env_settings.PAYPAL_SANDBOX_API_SIGNATURE
    PAYPAL_API_APPLICATION_ID = env_settings.PAYPAL_SANDBOX_API_APPLICATION_ID
    PAYPAL_API_EMAIL = env_settings.PAYPAL_SANDBOX_API_EMAIL
    PAYPAL_FRESPO_RECEIVER_EMAIL = env_settings.PAYPAL_SANDBOX_FRESPO_RECEIVER_EMAIL
else:
    PAYPAL_API_USERNAME = env_settings.PAYPAL_PRODUCTION_API_USERNAME
    PAYPAL_API_PASSWORD = env_settings.PAYPAL_PRODUCTION_API_PASSWORD
    PAYPAL_API_SIGNATURE = env_settings.PAYPAL_PRODUCTION_API_SIGNATURE
    PAYPAL_API_APPLICATION_ID = env_settings.PAYPAL_PRODUCTION_API_APPLICATION_ID
    PAYPAL_API_EMAIL = env_settings.PAYPAL_PRODUCTION_API_EMAIL
    PAYPAL_FRESPO_RECEIVER_EMAIL = env_settings.PAYPAL_PRODUCTION_FRESPO_RECEIVER_EMAIL



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = env_settings.TIME_ZONE

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*bz++cf(*#++vpo+b+=m3%p9#*x$$&amp;0mjs90x3oo5u@^zyvh)0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'core.context_processors.addAFewFrespoSettings',
)

ROOT_URLCONF = 'frespo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'frespo.wsgi.application'

PROJECT_DIR = os.path.dirname(__file__)+'/..'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates")
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
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
    'core',
#    'bootstrap-pagination'
    'pagination',
    'social_auth',
    'mailer',
    'south',
    'emailmgr',
)



AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
#    'social_auth.backends.contrib.skyrock.SkyrockBackend',
    'social_auth.backends.contrib.flickr.FlickrBackend',
    'social_auth.backends.contrib.instagram.InstagramBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.bitbucket.BitbucketBackend',
    'social_auth.backends.contrib.yandex.YandexBackend',
#    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    'social_auth.backends.OpenIDBackend',
    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
#    'social_auth.backends.contrib.douban.DoubanBackend',
    'social_auth.backends.browserid.BrowserIDBackend',
#    'social_auth.backends.contrib.vkontakte.VKontakteBackend',
#    'social_auth.backends.contrib.yandex.YandexOAuth2Backend',
    'social_auth.backends.contrib.yandex.YaruBackend',
#    'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiBackend',
#    'social_auth.backends.contrib.vkontakte.VKontakteOAuth2Backend',
#    'social_auth.backends.contrib.mailru.MailruBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TWITTER_CONSUMER_KEY         = env_settings.TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET      = env_settings.TWITTER_CONSUMER_SECRET
FACEBOOK_APP_ID              = env_settings.FACEBOOK_APP_ID
FACEBOOK_API_SECRET          = env_settings.FACEBOOK_API_SECRET
LINKEDIN_CONSUMER_KEY        = ''
LINKEDIN_CONSUMER_SECRET     = ''
ORKUT_CONSUMER_KEY           = ''
ORKUT_CONSUMER_SECRET        = ''
GOOGLE_CONSUMER_KEY          = ''
GOOGLE_CONSUMER_SECRET       = ''
GOOGLE_OAUTH2_CLIENT_ID      = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''
FOURSQUARE_CONSUMER_KEY      = ''
FOURSQUARE_CONSUMER_SECRET   = ''
GITHUB_APP_ID                = env_settings.GITHUB_APP_ID
GITHUB_API_SECRET            = env_settings.GITHUB_API_SECRET
DROPBOX_APP_ID               = ''
DROPBOX_API_SECRET           = ''
FLICKR_APP_ID                = ''
FLICKR_API_SECRET            = ''
INSTAGRAM_CLIENT_ID          = ''
INSTAGRAM_CLIENT_SECRET      = ''
VK_APP_ID                    = ''
VK_API_SECRET                = ''
BITBUCKET_CONSUMER_KEY       = env_settings.BITBUCKET_CONSUMER_KEY
BITBUCKET_CONSUMER_SECRET    = env_settings.BITBUCKET_CONSUMER_SECRET
LIVE_CLIENT_ID               = ''
LIVE_CLIENT_SECRET           = ''
SKYROCK_CONSUMER_KEY         = ''
SKYROCK_CONSUMER_SECRET      = ''
YAHOO_CONSUMER_KEY           = ''
YAHOO_CONSUMER_SECRET        = ''

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
FACEBOOK_EXTENDED_PERMISSIONS = ['email',]

LOGIN_URL          = '/core/login'
LOGIN_REDIRECT_URL = '/'
#LOGIN_ERROR_URL    = '/login-error/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': env_settings.FRESPO_LOG_FILE,
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
        'django.db': {
            'handlers': ['null'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

PAGINATION_DEFAULT_PAGINATION = 20
PAGINATION_DEFAULT_WINDOW = 3

