#this is a test settings for this app
import os
CUR_DIR = os.path.abspath(os.path.dirname(__file__))

PROJECT_NAME = "EmailMgr"
DEBUG = TEMPLATE_DEBUG = True
MAIN_DOMAIN_NAME = "example.com"
SITE_ID = 1
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': MAIN_DOMAIN_NAME.strip().split(".")[0]+"_db"
    }
}
INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'emailmgr',
    'south',
]
ROOT_URLCONF = 'emailmgr.urls'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

TEMPLATE_DIRS = os.path.join(CUR_DIR, "templates")

EMAIL_HOST = "localhost"
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = '%s <noreply@%s>' % (PROJECT_NAME, MAIN_DOMAIN_NAME)



