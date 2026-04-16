"""
Test Django + Supabase integration
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.conf import settings
from apps.library.supabase_client import supabase

def test_django_settings():
    """Test Django settings have Supabase config"""
    print("=" * 50)
    print("Testing Django Settings")
    print("=" * 50)
    
    checks = [
        ('SUPABASE_URL', settings.SUPABASE_URL),
        ('SUPABASE_KEY', settings.SUPABASE_KEY),
        ('SUPABASE_PROJECT_REF', settings.SUPABASE_PROJECT_REF),
    ]
    
    all_set = True
    for name, value in checks:
        if value:
            display = value[:30] + '...' if len(value) > 30 else value
            print(f"✓ {name}: {display}")
        else:
            print(f"✗ {name}: NOT SET")
            all_set = False
    
    return all_set

def test_supabase_client():
    """Test Supabase client works"""
    print("\n" + "=" * 50)
    print("Testing Supabase Client")
    print("=" * 50)
    
    try:
        client = supabase()
        print("✓ Supabase client created")
        
        # Test query
        response = client.table('library_book').select('count').execute()
        print("✓ Database query successful")
        
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_middleware():
    """Test middleware is configured"""
    print("\n" + "=" * 50)
    print("Testing Middleware Configuration")
    print("=" * 50)
    
    middleware = settings.MIDDLEWARE
    supabase_middleware = 'apps.library.supabase_middleware.SupabaseSessionMiddleware'
    
    if supabase_middleware in middleware:
        print(f"✓ Supabase middleware configured")
        return True
    else:
        print(f"✗ Supabase middleware not found")
        return False

def test_auth_backend():
    """Test authentication backend is configured"""
    print("\n" + "=" * 50)
    print("Testing Authentication Backend")
    print("=" * 50)
    
    backends = settings.AUTHENTICATION_BACKENDS
    supabase_backend = 'apps.library.supabase_auth.SupabaseAuthBackend'
    
    if supabase_backend in backends:
        print(f"✓ Supabase auth backend configured")
        return True
    else:
        print(f"✗ Supabase auth backend not found")
        return False

def test_models():
    """Test Django models are accessible"""
    print("\n" + "=" * 50)
    print("Testing Django Models")
    print("=" * 50)
    
    try:
        from apps.library.models import Book, Member, Category
        
        print(f"✓ Book model: {Book._meta.db_table}")
        print(f"✓ Member model: {Member._meta.db_table}")
        print(f"✓ Category model: {Category._meta.db_table}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to import models: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("DJANGO + SUPABASE INTEGRATION TEST")
    print("=" * 50 + "\n")
    
    results = []
    
    results.append(("Django Settings", test_django_settings()))
    results.append(("Supabase Client", test_supabase_client()))
    results.append(("Middleware", test_middleware()))
    results.append(("Auth Backend", test_auth_backend()))
    results.append(("Django Models", test_models()))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Django + Supabase integration is working!")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Please check the errors above")
    print("=" * 50 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
