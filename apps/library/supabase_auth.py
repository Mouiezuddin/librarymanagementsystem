"""
Supabase authentication backend for Django
"""
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .supabase_client import supabase


class SupabaseAuthBackend(BaseBackend):
    """
    Authenticate against Supabase Auth
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user with Supabase
        """
        if username is None or password is None:
            return None
        
        try:
            # Authenticate with Supabase
            response = supabase().auth.sign_in_with_password({
                "email": username,
                "password": password
            })
            
            if response.user:
                # Get or create Django user
                user, created = User.objects.get_or_create(
                    username=response.user.email,
                    defaults={
                        'email': response.user.email,
                        'first_name': response.user.user_metadata.get('first_name', ''),
                        'last_name': response.user.user_metadata.get('last_name', ''),
                    }
                )
                
                # Store Supabase session in request
                if request:
                    request.session['supabase_access_token'] = response.session.access_token
                    request.session['supabase_refresh_token'] = response.session.refresh_token
                
                return user
        except Exception as e:
            print(f"Supabase authentication error: {e}")
            return None
    
    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
