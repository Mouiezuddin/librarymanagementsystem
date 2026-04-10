import os
from .base import *

DEBUG = False

# Only allow localhost/127.0.0.1 for production-like testing on Windows
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', os.environ.get('ALLOWED_HOSTS', '')]

# Security Settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = False  # Set to True if using HTTPS/proxy
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'

# WhiteNoise Configuration for Static Files
# Insert whitenoise middleware right after SecurityMiddleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Production Email (Example)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ENABLE_PUBLIC_REGISTRATION = False
ENABLE_SEED_TOOLS = False
ENABLE_DEMO_DATA = False
