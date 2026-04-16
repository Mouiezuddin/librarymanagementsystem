# Supabase Quick Reference

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install supabase

# 2. Test connection
python test_supabase_connection.py

# 3. Sync existing data (optional)
python manage.py sync_to_supabase
```

## 🔑 Credentials

```bash
Project URL: https://otnctayrocscihsmhhcs.supabase.co
Project Ref: otnctayrocscihsmhhcs
Dashboard: https://supabase.com/dashboard/project/otnctayrocscihsmhhcs
```

## 📊 Database Tables

| Table | Description |
|-------|-------------|
| `auth_user` | Django user authentication |
| `library_category` | Book categories |
| `library_book` | Books with inventory |
| `library_member` | Library members |
| `library_bookissue` | Borrowing records |
| `library_notification` | User notifications |

## 💻 Code Examples

### Using Supabase Client

```python
from apps.library.supabase_client import supabase

# SELECT
books = supabase().table('library_book').select('*').execute()

# INSERT
supabase().table('library_book').insert({
    'title': 'New Book',
    'author': 'Author',
    'isbn': '1234567890',
    'total_copies': 5,
    'available_copies': 5
}).execute()

# UPDATE
supabase().table('library_book').update({
    'available_copies': 3
}).eq('id', 1).execute()

# DELETE
supabase().table('library_book').delete().eq('id', 1).execute()

# FILTER
books = supabase().table('library_book')\
    .select('*')\
    .eq('category_id', 1)\
    .gte('available_copies', 1)\
    .execute()
```

### Using Django ORM (Recommended)

```python
from apps.library.models import Book, Member

# Query
books = Book.objects.filter(available_copies__gt=0)
member = Member.objects.get(member_id='M001')

# Create
book = Book.objects.create(
    title='New Book',
    author='Author',
    isbn='1234567890'
)

# Update
book.available_copies = 3
book.save()

# Delete
book.delete()
```

### Authentication

```python
from apps.library.supabase_client import supabase

# Sign Up
response = supabase().auth.sign_up({
    'email': 'user@example.com',
    'password': 'secure_password',
    'options': {
        'data': {
            'first_name': 'John',
            'last_name': 'Doe'
        }
    }
})

# Sign In (use Django's authenticate)
from django.contrib.auth import authenticate
user = authenticate(username='user@example.com', password='password')

# Sign Out
supabase().auth.sign_out()

# Get Current User
user = supabase().auth.get_user()
```

### In Views

```python
def my_view(request):
    # Access via request
    books = request.supabase.table('library_book').select('*').execute()
    
    return render(request, 'books.html', {
        'books': books.data
    })
```

## 🔧 Management Commands

```bash
# Sync all data
python manage.py sync_to_supabase

# Sync specific model
python manage.py sync_to_supabase --model=book
python manage.py sync_to_supabase --model=member
python manage.py sync_to_supabase --model=category
```

## 🛠️ Common Operations

### Query with Filters

```python
# Books by category
books = supabase().table('library_book')\
    .select('*')\
    .eq('category_id', 1)\
    .execute()

# Available books
books = supabase().table('library_book')\
    .select('*')\
    .gt('available_copies', 0)\
    .execute()

# Search by title
books = supabase().table('library_book')\
    .select('*')\
    .ilike('title', '%python%')\
    .execute()

# Join with category
books = supabase().table('library_book')\
    .select('*, library_category(*)')\
    .execute()

# Order and limit
books = supabase().table('library_book')\
    .select('*')\
    .order('title')\
    .limit(10)\
    .execute()
```

### Aggregations

```python
# Count
count = supabase().table('library_book')\
    .select('*', count='exact')\
    .execute()
total = count.count

# Sum (use RPC function)
# Create function in Supabase SQL Editor first
```

### Real-time Subscriptions

```python
# Subscribe to changes
def handle_change(payload):
    print(f"Change detected: {payload}")

supabase().table('library_book')\
    .on('INSERT', handle_change)\
    .subscribe()
```

## 🔐 Security

### RLS Policies

All tables have Row Level Security enabled:

- **Public read** for books and categories
- **Authenticated access** for member data
- **User-specific** for notifications
- **Service role** for admin operations

### Using Service Role Key

```python
import os
from supabase import create_client

# For admin operations only
admin_client = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
)

# Bypass RLS
admin_client.table('library_book').select('*').execute()
```

## 📝 Environment Variables

```bash
# Required
SUPABASE_URL=https://otnctayrocscihsmhhcs.supabase.co
SUPABASE_KEY=sb_publishable_0PUpfH1ZT2RWayRiod1Cqw_24WR56uo

# Optional (for admin operations)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# For direct database connection
SUPABASE_DB_PASSWORD=your_db_password
```

## 🐛 Troubleshooting

### Connection Issues

```python
# Test connection
python test_supabase_connection.py

# Check environment
import os
print(os.environ.get('SUPABASE_URL'))
print(os.environ.get('SUPABASE_KEY'))
```

### Permission Errors

```python
# Check if authenticated
user = supabase().auth.get_user()
print(user)

# Use service role for admin operations
# (Set SUPABASE_SERVICE_ROLE_KEY in environment)
```

### Import Errors

```bash
# Install package
pip install supabase

# Verify installation
pip list | grep supabase
```

## 📚 Resources

- **Full Guide**: `SUPABASE_SETUP.md`
- **Summary**: `SUPABASE_INTEGRATION_SUMMARY.md`
- **Dashboard**: https://supabase.com/dashboard/project/otnctayrocscihsmhhcs
- **Docs**: https://supabase.com/docs
- **Python Client**: https://github.com/supabase-community/supabase-py

## 🎯 Next Steps

1. ✅ Install: `pip install supabase`
2. ✅ Test: `python test_supabase_connection.py`
3. ✅ Configure Django settings (see `config/settings/supabase_config.py`)
4. ✅ Sync data: `python manage.py sync_to_supabase`
5. ⬜ Explore dashboard
6. ⬜ Implement real-time features
7. ⬜ Set up file storage

---

**Need help?** Check `SUPABASE_SETUP.md` for detailed instructions.
