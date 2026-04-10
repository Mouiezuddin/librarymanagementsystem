from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Use console backend for emails in local dev
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ENABLE_PUBLIC_REGISTRATION = True
ENABLE_SEED_TOOLS = True
ENABLE_DEMO_DATA = True
