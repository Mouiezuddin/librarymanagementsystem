"""
Test script to verify Supabase connection and setup
Run this after setting up environment variables
"""
import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_environment():
    """Test if environment variables are set"""
    print("=" * 50)
    print("Testing Environment Variables")
    print("=" * 50)
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_KEY',
        'SUPABASE_PROJECT_REF'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var:
                display_value = value[:20] + '...' if len(value) > 20 else value
            else:
                display_value = value
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: NOT SET")
            all_set = False
    
    return all_set

def test_supabase_import():
    """Test if supabase package is installed"""
    print("\n" + "=" * 50)
    print("Testing Supabase Package")
    print("=" * 50)
    
    try:
        import supabase
        print(f"✓ Supabase package installed (version: {supabase.__version__ if hasattr(supabase, '__version__') else 'unknown'})")
        return True
    except ImportError as e:
        print(f"✗ Supabase package not installed: {e}")
        print("  Run: pip install supabase")
        return False

def test_client_creation():
    """Test if Supabase client can be created"""
    print("\n" + "=" * 50)
    print("Testing Supabase Client Creation")
    print("=" * 50)
    
    try:
        from apps.library.supabase_client import supabase
        client = supabase()
        print("✓ Supabase client created successfully")
        return True, client
    except Exception as e:
        print(f"✗ Failed to create Supabase client: {e}")
        return False, None

def test_database_connection(client):
    """Test database connection"""
    print("\n" + "=" * 50)
    print("Testing Database Connection")
    print("=" * 50)
    
    try:
        # Try to query a table
        response = client.table('library_book').select('count').execute()
        print(f"✓ Successfully connected to database")
        print(f"  Books table exists and is accessible")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_tables_exist(client):
    """Test if all required tables exist"""
    print("\n" + "=" * 50)
    print("Testing Database Tables")
    print("=" * 50)
    
    tables = [
        'library_category',
        'library_book',
        'library_member',
        'library_bookissue',
        'library_notification',
        'auth_user'
    ]
    
    all_exist = True
    for table in tables:
        try:
            response = client.table(table).select('count').limit(1).execute()
            print(f"✓ {table}: exists")
        except Exception as e:
            print(f"✗ {table}: not found or not accessible")
            all_exist = False
    
    return all_exist

def test_insert_and_delete(client):
    """Test insert and delete operations"""
    print("\n" + "=" * 50)
    print("Testing Write Operations")
    print("=" * 50)
    
    try:
        # Test category insert
        test_data = {
            'name': f'Test Category {os.urandom(4).hex()}',
            'description': 'This is a test category'
        }
        
        response = client.table('library_category').insert(test_data).execute()
        inserted_id = response.data[0]['id']
        print(f"✓ Insert operation successful (ID: {inserted_id})")
        
        # Test delete
        client.table('library_category').delete().eq('id', inserted_id).execute()
        print(f"✓ Delete operation successful")
        
        return True
    except Exception as e:
        print(f"✗ Write operations failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("SUPABASE CONNECTION TEST")
    print("=" * 50 + "\n")
    
    # Load environment from .env.supabase if exists
    env_file = os.path.join(os.path.dirname(__file__), '.env.supabase')
    if os.path.exists(env_file):
        print(f"Loading environment from {env_file}")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print()
    
    results = []
    
    # Run tests
    results.append(("Environment Variables", test_environment()))
    results.append(("Supabase Package", test_supabase_import()))
    
    client_created, client = test_client_creation()
    results.append(("Client Creation", client_created))
    
    if client:
        results.append(("Database Connection", test_database_connection(client)))
        results.append(("Tables Exist", test_tables_exist(client)))
        results.append(("Write Operations", test_insert_and_delete(client)))
    
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
        print("Your Supabase integration is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Please check the errors above and:")
        print("1. Ensure environment variables are set")
        print("2. Install supabase: pip install supabase")
        print("3. Check your Supabase project is active")
    print("=" * 50 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
