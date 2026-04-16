# 🔐 Security Fix Guide - RLS Policies

## ⚠️ Current Security Warnings

Your Supabase database currently has **7 security warnings** about overly permissive RLS policies. These policies allow unrestricted access to all tables, which is fine for development but **not recommended for production**.

## 🎯 What Needs to be Fixed

All tables currently have policies like:
```sql
USING (true)  -- Allows everyone to do everything
```

This should be changed to:
```sql
USING (auth.role() = 'authenticated')  -- Only authenticated users
```

## 📋 Tables Affected

1. `auth_user` - User authentication data
2. `library_category` - Book categories
3. `library_book` - Books
4. `library_member` - Library members
5. `library_bookissue` - Book borrowing records
6. `library_notification` - User notifications

## 🔧 How to Fix

### Option 1: Run SQL Script in Supabase (Recommended)

1. **Open Supabase SQL Editor**
   - Go to: https://supabase.com/dashboard/project/otnctayrocscihsmhhcs
   - Click "SQL Editor" in the left sidebar

2. **Copy the SQL Script**
   - Open the file: `supabase_secure_rls_policies.sql`
   - Copy all the content

3. **Run the Script**
   - Paste into SQL Editor
   - Click "Run" button
   - Wait for success message

4. **Verify**
   - The script includes a verification query at the end
   - Check that all policies are updated

### Option 2: Keep Current Policies (Development Only)

If you're still in development and want to keep the permissive policies:

**⚠️ WARNING**: Only do this if:
- You're in development/testing phase
- Your database doesn't contain sensitive data
- You plan to fix this before production

## 🛡️ New Security Model

After applying the fix, your security will work like this:

### Public Access (No Authentication Required)
- ✅ **Read** books, categories, members, issues, notifications
- ❌ **Write** operations require authentication

### Authenticated Users
- ✅ **Full CRUD** on all library tables
- ✅ Can manage books, members, issues, notifications

### Service Role (Your Django App)
- ✅ **Full access** to everything
- Uses `SUPABASE_SERVICE_ROLE_KEY` from `.env`

### Regular Users
- ✅ Can view their own user profile
- ❌ Cannot view other users' profiles

## 📊 Policy Details

### Before (Current - Insecure)
```sql
-- Everyone can do everything
CREATE POLICY "Enable all operations for all roles" ON library_book
    FOR ALL USING (true);
```

### After (Secure)
```sql
-- Public can read
CREATE POLICY "Anyone can view books" ON library_book
    FOR SELECT USING (true);

-- Only authenticated can write
CREATE POLICY "Authenticated users can insert books" ON library_book
    FOR INSERT 
    WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');
```

## 🔍 Impact on Your Django App

### Will Your App Still Work?

**YES!** Your Django app will continue to work because:

1. **Django uses Service Role Key**
   - Your app uses `SUPABASE_SERVICE_ROLE_KEY`
   - Service role bypasses RLS policies
   - All operations will work as before

2. **No Code Changes Needed**
   - Your Python code doesn't need updates
   - All existing queries will work
   - Data sync will continue to work

### Testing After Fix

```bash
# Test that everything still works
python test_supabase_connection.py
python test_django_supabase.py

# Test Django app
python manage.py runserver
# Visit: http://127.0.0.1:8000/books/
```

## 🎯 Recommended Actions

### For Development (Now)
1. ⬜ Review the security warnings
2. ⬜ Understand the new policies
3. ⬜ Keep current policies if actively developing
4. ⬜ Plan to apply fixes before production

### For Production (Before Launch)
1. ⬜ Run `supabase_secure_rls_policies.sql` in SQL Editor
2. ⬜ Test all Django functionality
3. ⬜ Verify security advisors show no warnings
4. ⬜ Document the security model

## 📝 Step-by-Step Fix Instructions

### 1. Backup Current Policies (Optional)

In Supabase SQL Editor, run:
```sql
SELECT * FROM pg_policies WHERE schemaname = 'public';
```

Save the output for reference.

### 2. Apply New Policies

1. Open: https://supabase.com/dashboard/project/otnctayrocscihsmhhcs
2. Click: "SQL Editor" → "New query"
3. Copy content from: `supabase_secure_rls_policies.sql`
4. Paste and click "Run"

### 3. Verify Success

Run this query:
```sql
SELECT 
    tablename,
    policyname,
    cmd,
    roles
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename;
```

You should see policies like:
- "Anyone can view books" (SELECT)
- "Authenticated users can insert books" (INSERT)
- etc.

### 4. Test Your App

```bash
# Test connection
python test_supabase_connection.py

# Test Django
python manage.py runserver
```

Visit http://127.0.0.1:8000/books/ - should work normally!

### 5. Check Security Advisors

1. Go to Supabase Dashboard
2. Click "Database" → "Advisors"
3. Check "Security" tab
4. Should show 0 warnings (or only minor ones)

## 🆘 Troubleshooting

### If Django App Stops Working

**Problem**: "Permission denied" errors

**Solution**: Verify your app uses service role key:
```python
# In .env file
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### If Sync Command Fails

**Problem**: `sync_to_supabase` command fails

**Solution**: The command uses the service role key, so it should work. If not:
```bash
# Check environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.environ.get('SUPABASE_SERVICE_ROLE_KEY'))"
```

### If You Need to Revert

Run this to go back to permissive policies:
```sql
-- WARNING: Only for development!
DROP POLICY IF EXISTS "Anyone can view books" ON library_book;
DROP POLICY IF EXISTS "Authenticated users can insert books" ON library_book;
-- ... (drop all new policies)

CREATE POLICY "Enable all operations for all roles" ON library_book
    FOR ALL USING (true);
-- ... (repeat for other tables)
```

## 📚 Additional Resources

- [Supabase RLS Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [PostgreSQL RLS Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Security Best Practices](https://supabase.com/docs/guides/database/database-linter)

## ✅ Summary

| Aspect | Current | After Fix |
|--------|---------|-----------|
| Security Warnings | 7 warnings | 0 warnings |
| Public Read Access | ✅ Yes | ✅ Yes |
| Public Write Access | ⚠️ Yes (insecure) | ❌ No (secure) |
| Authenticated Write | ✅ Yes | ✅ Yes |
| Django App Impact | N/A | ✅ No impact |
| Code Changes Needed | N/A | ❌ None |

## 🎯 Decision Time

**Choose one:**

### Option A: Fix Now (Recommended for Production)
```bash
# Run the SQL script in Supabase SQL Editor
# File: supabase_secure_rls_policies.sql
```

### Option B: Fix Later (OK for Development)
```bash
# Continue developing with current policies
# Remember to fix before production launch
```

---

**Need help?** Check the troubleshooting section or refer to Supabase documentation.
