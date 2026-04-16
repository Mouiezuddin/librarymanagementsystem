from .base import *
import os

DEBUG = False

# Security Settings
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError("The SECRET_KEY environment variable must be set in production.")

ALLOWED_HOSTS = get_list_env('ALLOWED_HOSTS')
if not ALLOWED_HOSTS:
    # Fallback to local if testing production-like mode locally
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CSRF & Session Security
CSRF_TRUSTED_ORIGINS = get_list_env('CSRF_TRUSTED_ORIGINS', 'https://librarymanagementsystem-0cty.onrender.com')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = get_bool_env('SECURE_SSL_REDIRECT', default=True)  # Enforce HTTPS in production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# WhiteNoise Configuration for Static Files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# WhiteNoise storage to compress and cache static files
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Database configuration
# Priority: Supabase PostgreSQL > DATABASE_URL > SQLite fallback
supabase_url = os.environ.get('SUPABASE_URL', '')
supabase_key = os.environ.get('SUPABASE_KEY', '')
supabase_project_ref = os.environ.get('SUPABASE_PROJECT_REF', 'otnctayrocscihsmhhcs')
supabase_db_password = os.environ.get('SUPABASE_DB_PASSWORD', '')
database_url = os.environ.get('DATABASE_URL', '')

# Log what we found (for debugging)
print(f"DEBUG: SUPABASE_URL present: {bool(supabase_url)}")
print(f"DEBUG: SUPABASE_KEY present: {bool(supabase_key)}")
print(f"DEBUG: SUPABASE_DB_PASSWORD present: {bool(supabase_db_password)}")
print(f"DEBUG: DATABASE_URL present: {bool(database_url)}")

if supabase_url and supabase_key and supabase_db_password:
    # Full Supabase PostgreSQL connection
    print("INFO: Using Supabase PostgreSQL database")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': supabase_db_password,
            'HOST': f'db.{supabase_project_ref}.supabase.co',
            'PORT': '5432',
            'OPTIONS': {
                'sslmode': 'require',
            },
            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,
        }
    }
elif database_url:
    # Fall back to DATABASE_URL (old Render PostgreSQL)
    print("INFO: Using DATABASE_URL for database connection")
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # SQLite fallback (Supabase client API will still work for queries)
    print("WARNING: Using SQLite fallback. Set SUPABASE_DB_PASSWORD for full PostgreSQL connection.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@nexalib.com')
