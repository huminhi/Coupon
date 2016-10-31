# Django settings for aaportal project.

DEBUG = True

SYS_SERVICE_URL = 'http://test-sysapi.lunextelecom.com/'
ATS_SERVICE_URL = 'http://test-sysapi.lunextelecom.com/'
API_SERVICE_URL = 'http://test-api.lunextelecom.com/'
POS_SERVICE_URL = 'http://test-api.lunextelecom.com/'
AUTH_SERVICE_URL = 'http://test-api.lunextelecom.com/AuthService.svc/'
SMS_URL = 'http://192.168.93.228:8081/sms/'

META_CONFIG_PATH = 'E:/Working/EclipseWorkspace/AdminPortal_2/src/lunex/aaportal/media'
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Khoa Tran', 'khoatran@lunextelecom.com'),
)

MANAGERS = ADMINS

DATABASES = {
#    'default': {
#        'NAME': ':memory:',
#        'ENGINE': 'sqlite3',
#    },
    'default': {
        'NAME': 'ats',
        'ENGINE': 'mysql',
        'USER': 'root',
        'PASSWORD': 'qazqaz',
        'HOST': 'localhost',
    },
    'topup_server': {
        'NAME': 'topup',
        'ENGINE': 'sql_server.pyodbc',
        'USER': 'dbadmin',
        'PASSWORD': 'dbadmin888',
        'HOST': '192.168.93.64'
    },
    'ats_server': {
        'NAME': 'ats',
        'ENGINE': 'mysql',
        'USER': 'root',
        'PASSWORD': 'qazqaz',
        'HOST': 'localhost',
    },
    'auth_server': {
        'NAME': 'auth',
        'ENGINE': 'mysql',
        'USER': 'root',
        'PASSWORD': 'qazqaz',
        'HOST': 'localhost',
    },
    'did_server': {
        'NAME': 'ExtApp',
        'ENGINE': 'sql_server.pyodbc',
        'USER': 'dbadmin',
        'PASSWORD': 'dbadmin888',
        'HOST': '192.168.93.64'
    },
    'sms_server': {
        'NAME': 'ExtApp',
        'ENGINE': 'sql_server.pyodbc',
        'USER': 'dbadmin',
        'PASSWORD': 'dbadmin888',
        'HOST': '192.168.93.64'
    },
    'lunex1_server': {
        'NAME': 'Lunexdev',
        'ENGINE': 'sql_server.pyodbc',
        'USER': 'dbadmin',
        'PASSWORD': 'dbadmin888',
        'HOST': '192.168.93.64'
    },
    'canada_portal': {
        'NAME': 'canadaportal', 'ENGINE': 'mysql', 
        'USER': 'lunexuser', 'PASSWORD': 'inn0v@tion', 
        'HOST': '192.168.93.19'
    },
    'classic_portal': {
        'NAME': 'classicportal', 'ENGINE': 'mysql',
        'USER': 'lunexuser', 'PASSWORD': 'inn0v@tion',
        'HOST': '192.168.93.19'
    },
    'gcs_portal': {
        'NAME': 'gpsportal', 'ENGINE': 'mysql',
        'USER': 'lunexuser', 'PASSWORD': 'inn0v@tion',
        'HOST': '192.168.93.19'
    },
    'max_portal': {
        'NAME': 'maxportal', 'ENGINE': 'mysql',
        'USER': 'lunexuser', 'PASSWORD': 'inn0v@tion',
        'HOST': '192.168.93.19'
    },
    'papa_portal': {
        'NAME': 'papaportal', 'ENGINE': 'mysql',
        'USER': 'lunexuser', 'PASSWORD': 'inn0v@tion',
        'HOST': '192.168.93.19'
    },
    'sit_portal': {
        'NAME': 'sitportal', 'ENGINE': 'mysql',
        'USER': 'lunexuser', 'PASSWORD': 'inn0v@tion',
        'HOST': '192.168.93.19'
    },
    'superprepaid_portal': {
        'NAME': 'superprepaidportal', 'ENGINE': 'mysql',
        'USER': 'lunexuser', 'PASSWORD': 'inn0v@tion',
        'HOST': '192.168.93.19'
    },
    'trueroots_portal': {
        'NAME': 'truerootsportal', 'ENGINE': 'mysql',
        'USER': 'lunexuser', 'PASSWORD': 'inn0v@tion',
        'HOST': '192.168.93.19'
    },
    'usa_portal': {
        'NAME': 'usaportal', 'ENGINE': 'mysql',
        'USER': 'lunexuser', 'PASSWORD': 'inn0v@tion',
        'HOST': '192.168.93.19'
    },
}

TEST_SYSTEM = True
AUTH_DB = 'auth_server'
AUTHENTICATION_BACKENDS = ('lunex.auth.backend.AuthMixedApiBackend',)
DATABASE_ROUTERS = ['lunex.aaportal.common.db_router.DbRouter']

DATABASE_ROUTES = {
                   'ats_server': ['lunex.aaportal.ats', 'lunex.aaportal.ats.plugins.report'],
                   'topup_server': ['lunex.topup', 'lunex.aaportal.topupgw'],
                   'did_server': ['lunex.aaportal.did', 'lunex.aaportal.admin_site.gui.report.sms'],
                   'sms_server': ['lunex.sms'],
                   'lunex1_server': ['lunex.aaportal.ecs'],
                   'canada_portal': ['lunex.aaportal.pos_portals.canada'],
                   'classic_portal': ['lunex.aaportal.pos_portals.classic'],
                   'gcs_portal': ['lunex.aaportal.pos_portals.gcs'],
                   'max_portal': ['lunex.aaportal.pos_portals.max'],
                   'papa_portal': ['lunex.aaportal.pos_portals.papa'],
                   'sit_portal': ['lunex.aaportal.pos_portals.sit'],
                   'superprepaid_portal': ['lunex.aaportal.pos_portals.superprepaid'],
                   'trueroots_portal': ['lunex.aaportal.pos_portals.trueroots'],
                   'usa_portal': ['lunex.aaportal.pos_portals.usa'],
                   'auth_server': ['django.contrib']
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/media/'
import os;
MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media/')
TEMPLATE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://static.lunextelecom.com/media/'
MEDIA_URL = 'https://app.lunexgroup.com/media/'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = 'http://static.lunextelecom.com/media/'
ADMIN_MEDIA_PREFIX = 'https://app.lunexgroup.com/media/'
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'av97=xibl77(7%o6j_l%ojvw3mugfw9yagd3n9h(iid#@2-muh'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'lunex.auth.middleware.AuthenticationMiddleware',
)

#CACHE_BACKEND = 'memcached://127.0.0.1:8000/'
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

ROOT_URLCONF = 'lunex.aaportal.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_ROOT
)

LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'

SESSION_COOKIE_AGE = 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGGING_OUTPUT = 'STDOUT'
LOGGING_LEVEL = 'DEBUG'
FROM_PHONE = '123423423'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    #'django.contrib.sites',
    'lunex.common',
    #'lunex.topup',
    #'lunex.aaportal.topupgw',
    #'lunex.aaportal.auth',
    #'lunex.aaportal.did',
    #'lunex.aaportal.ecs',
    'lunex.aaportal.ats.core',
    #'lunex.aaportal.ats.plugins.report',
    'lunex.aaportal.dms'
)

__INSTALLED_APPS = (    
    'lunex.aaportal.ats.core',
)

USAP_RESELLER = 'GA02D001'
MAXIMUM_LOWER_LEVELS = 3;

ECS_ALIAS_SKU = {
    '7000': '1020',
    '7001': '1000',
    '7002': '1020',
    '1211' : '1000',
    '1212' : '1000',
}

REVERSE_ACH_USER = 'lunex'
