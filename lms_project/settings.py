"""
Django settings for LibraMS — Library Management System
BCA Project 2023-2026 | Smt Kumudben Darbar College
"""

from pathlib import Path
import importlib.util
import os
from urllib.parse import parse_qs, unquote, urlparse

BASE_DIR = Path(__file__).resolve().parent.parent


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

# ── Security ──────────────────────────────────────────────────────────────────
DEBUG = _get_bool_env('DEBUG', default=True)

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'dev-only-secret-key-change-before-production-abc123xyz987'
    else:
        raise RuntimeError('SECRET_KEY must be set when DEBUG is False.')

ALLOWED_HOSTS = _get_list_env(
    'ALLOWED_HOSTS',
    '127.0.0.1,localhost' if DEBUG else ''
)
CSRF_TRUSTED_ORIGINS = _get_list_env('CSRF_TRUSTED_ORIGINS')
USE_WHITENOISE = _get_bool_env('USE_WHITENOISE', default=not DEBUG)
RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '').strip()

if RAILWAY_PUBLIC_DOMAIN:
    _append_unique(ALLOWED_HOSTS, RAILWAY_PUBLIC_DOMAIN)
    _append_unique(CSRF_TRUSTED_ORIGINS, f'https://{RAILWAY_PUBLIC_DOMAIN}')

if not DEBUG:
    _append_unique(ALLOWED_HOSTS, 'healthcheck.railway.app')

# ── Installed Apps ────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library.apps.LibraryConfig',
]

# ── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if USE_WHITENOISE and importlib.util.find_spec('whitenoise') is not None:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'lms_project.urls'

# ── Templates ─────────────────────────────────────────────────────────────────
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

WSGI_APPLICATION = 'lms_project.wsgi.application'
ASGI_APPLICATION = 'lms_project.asgi.application'

# ── Database ──────────────────────────────────────────────────────────────────
_database_url = os.environ.get('DATABASE_URL', '').strip()
_db_engine = os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3')
_db_conn_max_age = int(os.environ.get('DB_CONN_MAX_AGE', '0' if DEBUG else '60'))

if _database_url:
    DATABASES = {
        'default': _database_config_from_url(_database_url, BASE_DIR)
    }
elif _db_engine == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': _db_engine,
            'NAME': os.environ.get('DB_NAME', 'lms_db'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }

DATABASES['default']['CONN_MAX_AGE'] = _db_conn_max_age

# ── Auth ──────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
CSRF_COOKIE_SECURE = _get_bool_env('CSRF_COOKIE_SECURE', default=not DEBUG)
SESSION_COOKIE_SECURE = _get_bool_env('SESSION_COOKIE_SECURE', default=not DEBUG)
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = _get_bool_env('SECURE_SSL_REDIRECT', default=not DEBUG)
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '0' if DEBUG else '31536000'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = _get_bool_env(
    'SECURE_HSTS_INCLUDE_SUBDOMAINS',
    default=not DEBUG,
)
SECURE_HSTS_PRELOAD = _get_bool_env('SECURE_HSTS_PRELOAD', default=not DEBUG)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = os.environ.get('SECURE_REFERRER_POLICY', 'same-origin')
X_FRAME_OPTIONS = os.environ.get('X_FRAME_OPTIONS', 'DENY')

_proxy_ssl_header = os.environ.get('SECURE_PROXY_SSL_HEADER')
if _proxy_ssl_header:
    SECURE_PROXY_SSL_HEADER = (
        _proxy_ssl_header,
        os.environ.get('SECURE_PROXY_SSL_VALUE', 'https'),
    )
elif not DEBUG and RAILWAY_PUBLIC_DOMAIN:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ── Static & Media ────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

if USE_WHITENOISE and importlib.util.find_spec('whitenoise') is not None:
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }
    WHITENOISE_MAX_AGE = int(os.environ.get('WHITENOISE_MAX_AGE', '31536000'))

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Session ───────────────────────────────────────────────────────────────────
SESSION_COOKIE_AGE = 28800
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ── App-level Settings ────────────────────────────────────────────────────────
FINE_PER_DAY = int(os.environ.get('FINE_PER_DAY', 2))
DEFAULT_LOAN_DAYS = int(os.environ.get('DEFAULT_LOAN_DAYS', 14))
ENABLE_PUBLIC_REGISTRATION = _get_bool_env('ENABLE_PUBLIC_REGISTRATION', default=DEBUG)
ENABLE_SEED_TOOLS = _get_bool_env('ENABLE_SEED_TOOLS', default=DEBUG)
ENABLE_DEMO_DATA = _get_bool_env('ENABLE_DEMO_DATA', default=DEBUG)

# ── Messages ──────────────────────────────────────────────────────────────────
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.DEBUG:   'debug',
    message_constants.INFO:    'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR:   'error',
}

# ── Logging ───────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '[{asctime}] {levelname} {name}: {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'file': {'class': 'logging.FileHandler', 'filename': BASE_DIR / 'lms.log', 'formatter': 'verbose'},
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'WARNING'},
        'library': {'handlers': ['console', 'file'], 'level': 'DEBUG' if DEBUG else 'INFO', 'propagate': False},
    },
}

# ── Email & Notifications ───────────────────────────────────────────────────
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = _get_bool_env('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = _get_bool_env('EMAIL_USE_SSL', default=False)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Nexa Lib Alerts <alerts@nexalib.com>')
