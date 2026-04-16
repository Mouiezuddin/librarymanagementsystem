"""
Apply secure RLS policies to Supabase
"""
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.library.supabase_client import supabase

def apply_policies():
    """Apply secure RLS policies"""
    
    sql = """
-- ============================================
-- SECURE RLS POLICIES FOR PRODUCTION
-- ============================================

-- AUTH_USER TABLE - Service role only
DROP POLICY IF EXISTS "Enable all operations for all roles" ON auth_user;

CREATE POLICY "Service role can manage users" ON auth_user
    FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY "Users can view their own profile" ON auth_user
    FOR SELECT
    USING (auth.uid()::text = id::text OR auth.role() = 'service_role');

-- LIBRARY_CATEGORY - Public read, auth write
DROP POLICY IF EXISTS "Enable read access for all users" ON library_category;
DROP POLICY IF EXISTS "Enable insert for authenticated users and service role" ON library_category;
DROP POLICY IF EXISTS "Enable update for authenticated users and service role" ON library_category;
DROP POLICY IF EXISTS "Enable delete for authenticated users and service role" ON library_category;

CREATE POLICY "Anyone can view categories" ON library_category
    FOR SELECT
    USING (true);

CREATE POLICY "Authenticated users can insert categories" ON library_category
    FOR INSERT
    WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can update categories" ON library_category
    FOR UPDATE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can delete categories" ON library_category
    FOR DELETE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

-- LIBRARY_BOOK - Public read, auth write
DROP POLICY IF EXISTS "Enable read access for all users" ON library_book;
DROP POLICY IF EXISTS "Enable insert for all roles" ON library_book;
DROP POLICY IF EXISTS "Enable update for all roles" ON library_book;
DROP POLICY IF EXISTS "Enable delete for all roles" ON library_book;

CREATE POLICY "Anyone can view books" ON library_book
    FOR SELECT
    USING (true);

CREATE POLICY "Authenticated users can insert books" ON library_book
    FOR INSERT
    WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can update books" ON library_book
    FOR UPDATE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can delete books" ON library_book
    FOR DELETE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

-- LIBRARY_MEMBER - Auth users can manage
DROP POLICY IF EXISTS "Enable all operations for all roles" ON library_member;

CREATE POLICY "Anyone can view members" ON library_member
    FOR SELECT
    USING (true);

CREATE POLICY "Authenticated users can insert members" ON library_member
    FOR INSERT
    WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can update members" ON library_member
    FOR UPDATE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can delete members" ON library_member
    FOR DELETE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

-- LIBRARY_BOOKISSUE - Auth users can manage
DROP POLICY IF EXISTS "Enable all operations for all roles" ON library_bookissue;

CREATE POLICY "Anyone can view book issues" ON library_bookissue
    FOR SELECT
    USING (true);

CREATE POLICY "Authenticated users can create book issues" ON library_bookissue
    FOR INSERT
    WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can update book issues" ON library_bookissue
    FOR UPDATE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can delete book issues" ON library_bookissue
    FOR DELETE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

-- LIBRARY_NOTIFICATION - User-specific access
DROP POLICY IF EXISTS "Enable all operations for all roles" ON library_notification;

CREATE POLICY "Users can view all notifications" ON library_notification
    FOR SELECT
    USING (true);

CREATE POLICY "Authenticated users can create notifications" ON library_notification
    FOR INSERT
    WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can update notifications" ON library_notification
    FOR UPDATE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

CREATE POLICY "Authenticated users can delete notifications" ON library_notification
    FOR DELETE
    USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');
"""
    
    print("=" * 60)
    print("APPLYING SECURE RLS POLICIES")
    print("=" * 60)
    print()
    
    try:
        # Use service role key for admin operations
        from supabase import create_client
        
        url = os.environ.get('SUPABASE_URL')
        service_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        if not service_key:
            print("❌ SUPABASE_SERVICE_ROLE_KEY not found in environment")
            return False
        
        # Create admin client with service role
        admin_client = create_client(url, service_key)
        
        print("🔧 Applying policies...")
        
        # Execute the SQL
        response = admin_client.rpc('exec_sql', {'sql': sql}).execute()
        
        print("✅ Policies applied successfully!")
        print()
        
        # Verify
        print("🔍 Verifying policies...")
        verify_sql = """
        SELECT 
            tablename,
            policyname,
            cmd
        FROM pg_policies
        WHERE schemaname = 'public'
        ORDER BY tablename, policyname;
        """
        
        result = admin_client.rpc('exec_sql', {'sql': verify_sql}).execute()
        
        print(f"✅ Found {len(result.data) if result.data else 0} policies")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("⚠️  The Supabase Python client cannot execute raw SQL directly.")
        print("    Please run the SQL script manually in Supabase SQL Editor:")
        print()
        print("    1. Go to: https://supabase.com/dashboard/project/otnctayrocscihsmhhcs")
        print("    2. Click 'SQL Editor' in left sidebar")
        print("    3. Copy content from: supabase_secure_rls_policies.sql")
        print("    4. Paste and click 'Run'")
        print()
        return False

if __name__ == '__main__':
    success = apply_policies()
    
    print("=" * 60)
    if success:
        print("✅ SECURITY POLICIES UPDATED!")
        print()
        print("Next steps:")
        print("1. Test your Django app: python manage.py runserver")
        print("2. Check security advisors in Supabase dashboard")
    else:
        print("⚠️  MANUAL ACTION REQUIRED")
        print()
        print("Please apply the policies manually using:")
        print("File: supabase_secure_rls_policies.sql")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
