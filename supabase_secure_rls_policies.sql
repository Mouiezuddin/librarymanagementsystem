-- ============================================
-- SECURE RLS POLICIES FOR PRODUCTION
-- ============================================
-- Run this in Supabase SQL Editor to fix security warnings
-- This replaces overly permissive policies with secure ones

-- ============================================
-- AUTH_USER TABLE - Service role only
-- ============================================
DROP POLICY IF EXISTS "Enable all operations for all roles" ON auth_user;

CREATE POLICY "Service role can manage users" ON auth_user
    FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY "Users can view their own profile" ON auth_user
    FOR SELECT
    USING (auth.uid()::text = id::text OR auth.role() = 'service_role');

-- ============================================
-- LIBRARY_CATEGORY - Public read, auth write
-- ============================================
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

-- ============================================
-- LIBRARY_BOOK - Public read, auth write
-- ============================================
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

-- ============================================
-- LIBRARY_MEMBER - Auth users can manage
-- ============================================
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

-- ============================================
-- LIBRARY_BOOKISSUE - Auth users can manage
-- ============================================
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

-- ============================================
-- LIBRARY_NOTIFICATION - User-specific access
-- ============================================
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

-- ============================================
-- VERIFICATION QUERY
-- ============================================
-- Run this to verify policies are applied
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
