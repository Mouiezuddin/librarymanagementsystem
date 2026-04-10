import os
from django.core.wsgi import get_wsgi_application

# Default to production for Waitress/Deployment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
