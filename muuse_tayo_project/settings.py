from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-k4-#4#*(5lw9uek(4fk2l90k)xvc!a&4)+3!_+$&i13qfw7n-n')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,testserver', cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard.apps.DashboardConfig',
    'jobs.apps.JobsConfig',
    'applicants.apps.ApplicantsConfig',
    'selection.apps.SelectionConfig',
    'interviews.apps.InterviewsConfig',
    'messages.apps.MessagesConfig',
    'users.apps.UsersConfig',
    'verifications.apps.VerificationsConfig',
    'reports.apps.ReportsConfig',
    'backups.apps.BackupsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'muuse_tayo_project.middleware.LoginRequiredMiddleware',
    'muuse_tayo_project.middleware.VerificationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'muuse_tayo_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'messages.context_processors.unread_message_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'muuse_tayo_project.wsgi.application'

DB_ENGINE = config('DB_ENGINE', default='sqlite')
if DB_ENGINE == 'oracle':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': config('ORACLE_NAME', default='ORCL'),
            'USER': config('ORACLE_USER', default='MUUSE_TAYO_ADMIN'),
            'PASSWORD': config('ORACLE_PASSWORD', default=''),
            'HOST': config('ORACLE_HOST', default='oracle-db-server.local'),
            'PORT': config('ORACLE_PORT', default='1521'),
            'OPTIONS': {
                'threaded': True,
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'users.SystemUser'
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'root'
LOGOUT_REDIRECT_URL = 'users:login'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

# Session persistence — keep users logged in for 30 days
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30   # 30 days in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False    # Don't expire when browser closes
SESSION_SAVE_EVERY_REQUEST = True          # Refresh the session timer on each visit
