# Quick Start Guide - Nexa Lib LMS

## For Local Development

### 1. Setup Environment

```bash
# Navigate to project directory
cd lms_project

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements/local.txt
```

### 2. Run Setup Script

```bash
python setup.py
```

This will:
- Run migrations
- Create demo admin user (username: `admin`, password: `admin123`)
- Set up initial data

### 3. Start Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/login/

### 4. Login

**Demo Admin Account:**
- Username: `admin`
- Password: `admin123`

**Note:** Demo accounts are only created when `ENABLE_DEMO_DATA=True` (default in local settings)

---

## For Production Deployment

### 1. Environment Variables

Create a `.env` file with:

```env
# Security
SECRET_KEY=your-secret-key-here-generate-with-django
DEBUG=False

# Hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (example for PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Features (disable in production)
ENABLE_PUBLIC_REGISTRATION=False
ENABLE_SEED_TOOLS=False
ENABLE_DEMO_DATA=False

# SSL
SECURE_SSL_REDIRECT=True
```

### 2. Generate SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

### 5. Run Deployment Checks

```bash
python manage.py check --deploy
```

### 6. Start with Gunicorn

```bash
gunicorn config.wsgi:application -c gunicorn.conf.py
```

---

## Common Commands

### Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Data Management
```bash
# Seed 500 books (development only)
python manage.py seed_data

# Update fines for overdue books
python manage.py update_fines

# Send reminder emails
python manage.py send_reminders

# Send overdue alerts
python manage.py send_alerts
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Testing
```bash
# Run tests
python manage.py test

# Check for issues
python manage.py check

# Check deployment readiness
python manage.py check --deploy
```

---

## Features Overview

### For Librarians/Admins
- ✅ Manage books (add, edit, delete)
- ✅ Manage members (register, edit, suspend)
- ✅ Issue books to members
- ✅ Process book returns
- ✅ Calculate and collect fines
- ✅ View reports and analytics
- ✅ Export data to CSV
- ✅ Send overdue alerts
- ✅ Manage categories

### For Members
- ✅ View available books
- ✅ Search and filter books
- ✅ View borrowing history
- ✅ Check due dates
- ✅ View fines
- ✅ Receive notifications
- ✅ Update profile

---

## Troubleshooting

### Issue: "SECRET_KEY must be set"
**Solution:** Set the `SECRET_KEY` environment variable or add it to `.env` file

### Issue: "ALLOWED_HOSTS validation failed"
**Solution:** Add your domain to `ALLOWED_HOSTS` in environment variables

### Issue: "Database connection failed"
**Solution:** Check `DATABASE_URL` or database settings in `.env`

### Issue: "Static files not loading"
**Solution:** Run `python manage.py collectstatic --noinput`

### Issue: "Email not sending"
**Solution:** Configure SMTP settings in environment variables

---

## Security Notes

⚠️ **IMPORTANT:**
1. Never commit `.env` files to version control
2. Always use strong, random `SECRET_KEY` in production
3. Set `DEBUG=False` in production
4. Disable demo features in production
5. Use HTTPS in production
6. Regular database backups
7. Keep dependencies updated

---

## Support

- **Documentation:** See `README.md`, `DEPLOYMENT.md`, `RENDER_DEPLOYMENT.md`
- **Security Report:** See `SECURITY_AND_FIXES_REPORT.md`
- **Django Docs:** https://docs.djangoproject.com/

---

**Version:** 1.0  
**Last Updated:** April 15, 2026
