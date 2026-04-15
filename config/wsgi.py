import os
from django.core.wsgi import get_wsgi_application

# Default to production settings, override with DJANGO_SETTINGS_MODULE env var if needed
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
