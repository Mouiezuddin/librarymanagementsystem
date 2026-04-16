# Supabase Architecture for Django LMS

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Django LMS Application                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Views      │  │   Models     │  │  Templates   │      │
│  │              │  │              │  │              │      │
│  │  - book_list │  │  - Book      │  │  - base.html │      │
│  │  - member    │  │  - Member    │  │  - books.html│      │
│  │  - issue     │  │  - Issue     │  │  - ...       │      │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘      │
│         │                  │                                 │
│         └──────────┬───────┘                                 │
│                    │                                         │
│  ┌─────────────────▼────────────────────────────────┐       │
│  │         Django ORM / Supabase Client             │       │
│  ├──────────────────────────────────────────────────┤       │
│  │  • supabase_client.py                            │       │
│  │  • supabase_auth.py (Authentication Backend)     │       │
│  │  • supabase_middleware.py (Session Management)   │       │
│  └─────────────────┬────────────────────────────────┘       │
│                    │                                         │
└────────────────────┼─────────────────────────────────────────┘
                     │
                     │ HTTPS / REST API
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                    Supabase Platform                          │
│         https://otnctayrocscihsmhhcs.supabase.co             │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              PostgreSQL Database                      │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  Tables:                                              │   │
│  │  • auth_user                                          │   │
│  │  • library_category                                   │   │
│  │  • library_book                                       │   │
│  │  • library_member                                     │   │
│  │  • library_bookissue                                  │   │
│  │  • library_notification                               │   │
│  │                                                        │   │
│  │  Features:                                             │   │
│  │  • Row Level Security (RLS)                           │   │
│  │  • Foreign Keys & Constraints                         │   │
│  │  • Indexes for Performance                            │   │
│  │  • Triggers & Functions                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Supabase Auth                            │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  • User Registration                                  │   │
│  │  • Email/Password Authentication                      │   │
│  │  • JWT Token Management                               │   │
│  │  • Session Handling                                   │   │
│  │  • OAuth Providers (Optional)                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Supabase Storage (Optional)              │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  • Book Cover Images                                  │   │
│  │  • Member Photos                                      │   │
│  │  • Document Uploads                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Realtime (Optional)                      │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  • Live Book Availability Updates                     │   │
│  │  • Notification Broadcasts                            │   │
│  │  • Real-time Dashboard                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Authentication Flow

```
User Login Request
       │
       ▼
Django View (login)
       │
       ▼
SupabaseAuthBackend.authenticate()
       │
       ▼
Supabase Auth API
       │
       ▼
JWT Token Generated
       │
       ▼
Session Stored in Django
       │
       ▼
User Authenticated
```

### 2. Data Query Flow (Django ORM)

```
View: Book.objects.all()
       │
       ▼
Django ORM
       │
       ▼
PostgreSQL Query
       │
       ▼
Supabase PostgreSQL
       │
       ▼
RLS Policy Check
       │
       ▼
Data Returned
       │
       ▼
Django Model Instances
       │
       ▼
Template Rendering
```

### 3. Data Query Flow (Supabase Client)

```
View: supabase().table('library_book').select('*')
       │
       ▼
Supabase Python Client
       │
       ▼
REST API Request
       │
       ▼
Supabase API Gateway
       │
       ▼
RLS Policy Check
       │
       ▼
PostgreSQL Query
       │
       ▼
JSON Response
       │
       ▼
Python Dict/List
       │
       ▼
Template Rendering
```

## Component Responsibilities

### Django Application Layer

**Views** (`apps/library/views.py`)
- Handle HTTP requests
- Business logic
- Call models or Supabase client
- Render templates

**Models** (`apps/library/models.py`)
- Define data structure
- Django ORM interface
- Model methods and properties
- Validation

**Supabase Client** (`apps/library/supabase_client.py`)
- Initialize Supabase connection
- Singleton pattern
- Direct API access

**Auth Backend** (`apps/library/supabase_auth.py`)
- Authenticate users with Supabase
- Sync Django users
- Manage sessions

**Middleware** (`apps/library/supabase_middleware.py`)
- Attach Supabase client to requests
- Handle session tokens
- Refresh expired tokens

### Supabase Platform Layer

**PostgreSQL Database**
- Store all application data
- Enforce constraints
- Execute queries
- Maintain relationships

**Row Level Security (RLS)**
- Policy-based access control
- User-level data isolation
- Secure by default

**Supabase Auth**
- User management
- JWT token generation
- Session handling
- OAuth integration

**REST API**
- Auto-generated from schema
- CRUD operations
- Real-time subscriptions
- File uploads

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Layer 1: Django Authentication                          │
│  ├─ Session-based auth                                   │
│  ├─ CSRF protection                                      │
│  └─ Permission checks                                    │
│                                                           │
│  Layer 2: Supabase JWT Authentication                    │
│  ├─ Token validation                                     │
│  ├─ User identity verification                           │
│  └─ Role-based access                                    │
│                                                           │
│  Layer 3: Row Level Security (RLS)                       │
│  ├─ Table-level policies                                 │
│  ├─ User-specific data access                            │
│  └─ Automatic enforcement                                │
│                                                           │
│  Layer 4: Database Constraints                           │
│  ├─ Foreign key constraints                              │
│  ├─ Check constraints                                    │
│  └─ Unique constraints                                   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## API Keys & Access Levels

```
┌──────────────────────────────────────────────────────────┐
│                      API Keys                             │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  Publishable Key (sb_publishable_...)                     │
│  ├─ Use: Client-side, public access                      │
│  ├─ Permissions: Respects RLS policies                   │
│  └─ Safe to expose in frontend                           │
│                                                            │
│  Service Role Key (eyJhbGciOiJIUzI1NiI...)               │
│  ├─ Use: Server-side, admin operations                   │
│  ├─ Permissions: Bypasses RLS policies                   │
│  └─ NEVER expose publicly                                │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

## Database Schema Relationships

```
┌─────────────┐
│  auth_user  │
└──────┬──────┘
       │
       │ 1:1
       │
┌──────▼──────────┐
│ library_member  │
└──────┬──────────┘
       │
       │ 1:N
       │
┌──────▼────────────┐      ┌──────────────────┐
│ library_bookissue │◄─────┤  library_book    │
└───────────────────┘  N:1 └────────┬─────────┘
                                     │
                                     │ N:1
                                     │
                            ┌────────▼──────────┐
                            │ library_category  │
                            └───────────────────┘

┌─────────────┐
│library_member│
└──────┬───────┘
       │
       │ 1:N
       │
┌──────▼──────────────────┐
│ library_notification    │
└─────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Production Setup                       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Django App (Render/Railway/Heroku)                      │
│       │                                                   │
│       ├─ Environment Variables                           │
│       │  ├─ SUPABASE_URL                                 │
│       │  ├─ SUPABASE_KEY                                 │
│       │  └─ SUPABASE_SERVICE_ROLE_KEY                    │
│       │                                                   │
│       └─ Database Connection                             │
│          └─ PostgreSQL (Supabase)                        │
│                                                           │
│  Supabase (Cloud Hosted)                                 │
│       │                                                   │
│       ├─ Database (PostgreSQL)                           │
│       ├─ Authentication                                   │
│       ├─ Storage                                          │
│       └─ Realtime                                         │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Integration Points

### 1. Django Settings Integration

```python
# config/settings/base.py
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

AUTHENTICATION_BACKENDS = [
    'apps.library.supabase_auth.SupabaseAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    # ...
    'apps.library.supabase_middleware.SupabaseSessionMiddleware',
    # ...
]
```

### 2. View Integration

```python
# Option A: Django ORM
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})

# Option B: Supabase Client
def book_list(request):
    books = request.supabase.table('library_book').select('*').execute()
    return render(request, 'books.html', {'books': books.data})
```

### 3. Authentication Integration

```python
# Login with Supabase
from django.contrib.auth import authenticate, login

def login_view(request):
    user = authenticate(
        username=request.POST['email'],
        password=request.POST['password']
    )
    if user:
        login(request, user)
        # Supabase session automatically stored
```

## Performance Considerations

### Database Indexes

```sql
-- Already created for optimal performance
CREATE INDEX idx_book_category ON library_book(category_id);
CREATE INDEX idx_bookissue_member ON library_bookissue(member_id);
CREATE INDEX idx_bookissue_status ON library_bookissue(status);
```

### Connection Pooling

```python
# Supabase client uses connection pooling automatically
# For Django ORM, configure in settings:
DATABASES = {
    'default': {
        # ...
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### Caching Strategy

```python
# Use Django cache for frequently accessed data
from django.core.cache import cache

def get_available_books():
    books = cache.get('available_books')
    if not books:
        books = Book.objects.filter(available_copies__gt=0)
        cache.set('available_books', books, 300)  # 5 minutes
    return books
```

## Monitoring & Logging

```
Supabase Dashboard
├─ Database Performance
│  ├─ Query performance
│  ├─ Connection stats
│  └─ Table sizes
│
├─ API Logs
│  ├─ Request logs
│  ├─ Error logs
│  └─ Performance metrics
│
└─ Auth Logs
   ├─ Login attempts
   ├─ User registrations
   └─ Token refreshes
```

---

This architecture provides a scalable, secure, and maintainable foundation for your Library Management System.
