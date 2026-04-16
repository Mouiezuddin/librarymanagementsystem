"""
Supabase client configuration for Django LMS
"""
import os
from supabase import create_client, Client
from django.conf import settings

# Initialize Supabase client
def get_supabase_client() -> Client:
    """
    Create and return a Supabase client instance
    """
    url = os.environ.get("SUPABASE_URL") or getattr(settings, 'SUPABASE_URL', None)
    key = os.environ.get("SUPABASE_KEY") or getattr(settings, 'SUPABASE_KEY', None)
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment or settings")
    
    return create_client(url, key)

# Singleton instance
_supabase_client = None

def supabase() -> Client:
    """
    Get the singleton Supabase client instance
    """
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = get_supabase_client()
    return _supabase_client
