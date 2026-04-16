"""
Supabase session middleware for Django
"""
import os
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class SupabaseSessionMiddleware(MiddlewareMixin):
    """
    Middleware to manage Supabase sessions
    """
    
    def process_request(self, request):
        """
        Attach Supabase client to request with session if available
        """
        # Only initialize Supabase if credentials are available
        supabase_url = os.environ.get('SUPABASE_URL') or getattr(settings, 'SUPABASE_URL', None)
        supabase_key = os.environ.get('SUPABASE_KEY') or getattr(settings, 'SUPABASE_KEY', None)
        
        if supabase_url and supabase_key:
            try:
                from .supabase_client import supabase
                request.supabase = supabase()
                
                # If user has Supabase tokens in session, set them
                access_token = request.session.get('supabase_access_token')
                refresh_token = request.session.get('supabase_refresh_token')
                
                if access_token and refresh_token:
                    try:
                        # Set session for this request
                        request.supabase.auth.set_session(access_token, refresh_token)
                    except Exception as e:
                        # Session expired or invalid, clear it
                        request.session.pop('supabase_access_token', None)
                        request.session.pop('supabase_refresh_token', None)
            except Exception as e:
                # Supabase not available, continue without it
                request.supabase = None
        else:
            # Supabase credentials not configured
            request.supabase = None
        
        return None
