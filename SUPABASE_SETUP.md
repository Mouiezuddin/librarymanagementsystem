# Supabase Integration Setup Guide

This guide explains how to use Supabase with your Django LMS project for database and authentication.

## Overview

Your Django LMS is now integrated with Supabase, providing:
- PostgreSQL database hosted on Supabase
- Row Level Security (RLS) for data protection
- Supabase Auth integration with Django authentication
- Real-time capabilities (optional)

## Configuration

### 1. Environment Variables

Add these variables to your `.env` file or environment:

```bash
# Supabase Configuration
SUPABASE_URL=https://otnctayrocscihsmhhcs.supabase.co
SUPABASE_KEY=sb_publishable_0PUpfH1ZT2RWayRiod1Cqw_24WR56uo
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90bmN0YXlyb2NzY2loc21oaGNzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjIzNTUxNywiZXhwIjoyMDkxODExNTE3fQ.8DT6f5J8Ae2CqGSin3YE1hrkOj7edyaAfF-g1sXWlhA
SUPABASE_PROJECT_REF=otnctayrocscihsmhhcs
```

### 2. Django Settings

Add to your `config/settings/base.py`:

```python
# Supabase Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

# Add Supabase authentication backend
AUTHENTICATION_BACKENDS = [
    'apps.library.supabase_auth.SupabaseAuthBackend',
    'django.contrib.auth.backends.ModelBackend',  # Keep Django auth as fallback
]

# Add Supabase middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.library.supabase_middleware.SupabaseSessionMiddleware',  # Add this
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### 3. Database Configuration

You can use Supabase as your primary database. Update your `DATABASES` setting:

```python
# Option 1: Use Supabase PostgreSQL directly
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('SUPABASE_DB_PASSWORD'),  # Get from Supabase dashboard
        'HOST': 'db.otnctayrocscihsmhhcs.supabase.co',
        'PORT': '5432',
    }
}

# Option 2: Keep SQLite for local development, use Supabase for production
# (Current setup - no changes needed)
```

## Database Schema

The following tables have been created in your Supabase database:

- `auth_user` - Django user authentication
- `library_category` - Book categories
- `library_book` - Books with inventory tracking
- `library_member` - Library members
- `library_bookissue` - Book borrowing records
- `library_notification` - User notifications

All tables have Row Level Security (RLS) enabled with appropriate policies.

## Using Supabase in Your Code

### 1. Direct Supabase Client

```python
from apps.library.supabase_client import supabase

# Query books
response = supabase().table('library_book').select('*').execute()
books = response.data

# Insert a new book
new_book = {
    'title': 'Python Programming',
    'author': 'John Doe',
    'isbn': '1234567890',
    'total_copies': 5,
    'available_copies': 5
}
supabase().table('library_book').insert(new_book).execute()
```

### 2. Django ORM (Recommended)

Continue using Django ORM as usual. The models will work with Supabase PostgreSQL:

```python
from apps.library.models import Book, Member

# Query using Django ORM
books = Book.objects.filter(available_copies__gt=0)
member = Member.objects.get(member_id='M001')
```

### 3. Authentication

Users can authenticate through Supabase Auth:

```python
# In your views
from apps.library.supabase_client import supabase

def register_user(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    # Register with Supabase
    response = supabase().auth.sign_up({
        'email': email,
        'password': password,
        'options': {
            'data': {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name')
            }
        }
    })
    
    return response
```

## Accessing Supabase in Requests

The middleware adds a `supabase` attribute to every request:

```python
def my_view(request):
    # Access Supabase client
    books = request.supabase.table('library_book').select('*').execute()
    return render(request, 'books.html', {'books': books.data})
```

## Supabase Dashboard

Access your Supabase project dashboard at:
https://supabase.com/dashboard/project/otnctayrocscihsmhhcs

From the dashboard you can:
- View and edit data in Table Editor
- Monitor database performance
- Manage authentication users
- Configure storage buckets
- View API logs
- Set up real-time subscriptions

## Migration from SQLite

To migrate your existing SQLite data to Supabase:

1. Export data from SQLite:
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data.json
```

2. Configure Django to use Supabase PostgreSQL (see Database Configuration above)

3. Run migrations:
```bash
python manage.py migrate
```

4. Import data:
```bash
python manage.py loaddata data.json
```

## Security Best Practices

1. **Never expose service role key** - Only use it server-side
2. **Use RLS policies** - Already configured for your tables
3. **Validate user input** - Always sanitize data before database operations
4. **Use environment variables** - Never commit credentials to git
5. **Enable MFA** - For Supabase dashboard access

## Troubleshooting

### Connection Issues
- Verify environment variables are set correctly
- Check Supabase project status in dashboard
- Ensure your IP is not blocked (check Supabase network settings)

### Authentication Issues
- Verify SUPABASE_KEY is the publishable key (starts with `sb_publishable_`)
- Check user exists in Supabase Auth dashboard
- Ensure authentication backend is configured in settings

### RLS Policy Issues
- Use service role key for admin operations
- Check policy definitions in Supabase SQL Editor
- Verify user authentication status

## Next Steps

1. Install Supabase Python client:
```bash
pip install -r requirements/base.txt
```

2. Update your Django settings as described above

3. Test the connection:
```bash
python manage.py shell
>>> from apps.library.supabase_client import supabase
>>> print(supabase().table('library_book').select('count').execute())
```

4. Consider using Supabase Storage for book cover images

5. Explore real-time features for live notifications

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
- [Django + Supabase Guide](https://supabase.com/docs/guides/getting-started/tutorials/with-django)
