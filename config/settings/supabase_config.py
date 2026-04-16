"""
Supabase configuration snippet for Django settings
Add these to your base.py or local.py settings file
"""
import os

# Supabase Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://otnctayrocscihsmhhcs.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'sb_publishable_0PUpfH1ZT2RWayRiod1Cqw_24WR56uo')
SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_PROJECT_REF = os.environ.get('SUPABASE_PROJECT_REF', 'otnctayrocscihsmhhcs')

# Optional: Use Supabase PostgreSQL as primary database
# Uncomment and configure with your database password from Supabase dashboard
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('SUPABASE_DB_PASSWORD'),
        'HOST': f'db.{SUPABASE_PROJECT_REF}.supabase.co',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}
"""

# Add Supabase authentication backend
# Add this to your AUTHENTICATION_BACKENDS list
AUTHENTICATION_BACKENDS = [
    'apps.library.supabase_auth.SupabaseAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Add Supabase middleware
# Add 'apps.library.supabase_middleware.SupabaseSessionMiddleware' to MIDDLEWARE
# after 'django.contrib.auth.middleware.AuthenticationMiddleware'
