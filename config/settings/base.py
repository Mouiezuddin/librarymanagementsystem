import os
import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

# BASE_DIR points to the project root (where manage.py sits)
# Since this file is in config/settings/, we go up 2 levels
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Add apps directory to sys.path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

def _get_bool_env(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}

def _get_list_env(name, default=''):
    value = os.environ.get(name, default)
    return [item.strip() for item in value.split(',') if item.strip()]

def _append_unique(items, value):
    if value and value not in items:
        items.append(value)

def _database_config_from_url(database_url, base_dir):
    parsed = urlparse(database_url)
    scheme = parsed.scheme.lower()
    engine_map = {
        'postgres': 'django.db.backends.postgresql',
        'postgresql': 'django.db.backends.postgresql',
        'pgsql': 'django.db.backends.postgresql',
        'mysql': 'django.db.backends.mysql',
        'mariadb': 'django.db.backends.mysql',
        'sqlite': 'django.db.backends.sqlite3',
        'sqlite3': 'django.db.backends.sqlite3',
    }
    engine = engine_map.get(scheme)
    if not engine:
        raise RuntimeError(f'Unsupported DATABASE_URL scheme: {scheme}')

    if engine == 'django.db.backends.sqlite3':
        db_path = unquote(parsed.path or '').lstrip('/')
        return {
            'ENGINE': engine,
            'NAME': base_dir / db_path if db_path else base_dir / 'db.sqlite3',
        }

    query_options = {key: values[-1] for key, values in parse_qs(parsed.query).items() if values}
    options = dict(query_options)
    if engine == 'django.db.backends.mysql' and 'charset' not in options:
        options['charset'] = 'utf8mb4'

    config = {
        'ENGINE': engine,
        'NAME': unquote((parsed.path or '').lstrip('/')),
        'USER': unquote(parsed.username or ''),
        'PASSWORD': unquote(parsed.password or ''),
        'HOST': parsed.hostname or '',
        'PORT': str(parsed.port or ''),
    }
    if options:
        config['OPTIONS'] = options
    return config

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-change-it')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library.apps.LibraryConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise goes here in production settings
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'library.context_processors.unread_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
_database_url = os.environ.get('DATABASE_URL', '').strip()
if _database_url:
    DATABASES = {'default': _database_config_from_url(_database_url, BASE_DIR)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# App Settings
FINE_PER_DAY = 2
DEFAULT_LOAN_DAYS = 14
