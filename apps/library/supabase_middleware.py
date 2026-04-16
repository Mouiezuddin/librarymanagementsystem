"""
Supabase session middleware for Django
"""
from django.utils.deprecation import MiddlewareMixin
from .supabase_client import supabase


class SupabaseSessionMiddleware(MiddlewareMixin):
    """
    Middleware to manage Supabase sessions
    """
    
    def process_request(self, request):
        """
        Attach Supabase client to request with session if available
        """
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
        
        return None
