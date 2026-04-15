# Render Deployment Guide

Service ID: `rnd_pN3e6R4cFE2I8GsNUg8KPaEQt8aU`

## Quick Setup Checklist

### 1. Render Web Service Configuration

In your Render dashboard for this service, configure:

**Build Command:**
```bash
pip install -r requirements/production.txt && python manage.py collectstatic --noinput
```

**Start Command:**
```bash
gunicorn config.wsgi:application -c gunicorn.conf.py
```

**Health Check Path:**
```
/health/
```

### 2. Environment Variables

Set these in Render dashboard under "Environment":

#### Required Variables:
```
SECRET_KEY=<generate-a-strong-random-key>
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
DATABASE_URL=<your-postgres-connection-string>
```

#### Recommended Variables:
```
ALLOWED_HOSTS=<your-render-domain>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<your-render-domain>.onrender.com
SECURE_SSL_REDIRECT=True
```

#### Optional App Settings:
```
FINE_PER_DAY=2
DEFAULT_LOAN_DAYS=14
ENABLE_PUBLIC_REGISTRATION=False
ENABLE_SEED_TOOLS=False
ENABLE_DEMO_DATA=False
```

#### Email Configuration (Optional):
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Library System <your-email@gmail.com>
```

### 3. Database Setup

Render provides PostgreSQL databases. To add one:

1. Go to Render Dashboard → New → PostgreSQL
2. Create database
3. Copy the "External Database URL"
4. Add it as `DATABASE_URL` environment variable in your web service

### 4. Pre-Deploy Commands

Add this as a "Pre-Deploy Command" in Render:
```bash
python manage.py migrate --noinput
```

### 5. Static Files

Static files are automatically handled by WhiteNoise. No additional configuration needed.

## Deployment Steps

1. **Push your code to GitHub** (if not already done)

2. **Connect to Render:**
   - Go to Render Dashboard
   - Select your service or create new Web Service
   - Connect your GitHub repository
   - Select branch (usually `main` or `master`)

3. **Configure Build & Start Commands** (see section 1 above)

4. **Set Environment Variables** (see section 2 above)

5. **Add Database** (see section 3 above)

6. **Deploy:**
   - Click "Manual Deploy" or push to trigger auto-deploy
   - Monitor logs for any errors

## Post-Deployment

### Create Superuser

After first deployment, use Render Shell:

```bash
python manage.py createsuperuser
```

### Verify Deployment

1. Visit `https://<your-service>.onrender.com/health/` - should return `{"status": "ok"}`
2. Visit `https://<your-service>.onrender.com/admin/` - admin panel should load
3. Login with superuser credentials

## Troubleshooting

### Static Files Not Loading
- Ensure `collectstatic` runs in build command
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- WhiteNoise should be in middleware (already configured)

### Database Connection Errors
- Verify `DATABASE_URL` is set correctly
- Check database is running and accessible
- Ensure `psycopg2-binary` is in requirements

### 500 Errors
- Check Render logs: Dashboard → Service → Logs
- Verify `SECRET_KEY` is set
- Ensure `ALLOWED_HOSTS` includes your Render domain
- Check `DEBUG=False` is set

### CSRF Errors
- Add your domain to `CSRF_TRUSTED_ORIGINS`
- Format: `https://your-domain.onrender.com` (with https://)

## Security Checklist

- ✅ `DEBUG=False`
- ✅ Strong `SECRET_KEY` (50+ random characters)
- ✅ `ALLOWED_HOSTS` configured
- ✅ `CSRF_TRUSTED_ORIGINS` configured
- ✅ `SECURE_SSL_REDIRECT=True`
- ✅ `ENABLE_PUBLIC_REGISTRATION=False`
- ✅ `ENABLE_SEED_TOOLS=False`
- ✅ `ENABLE_DEMO_DATA=False`

## Monitoring

- **Health Check:** `/health/` endpoint
- **Logs:** Available in Render Dashboard
- **Metrics:** Render provides CPU, memory, and request metrics

## Scaling

Render allows you to scale:
- **Vertical:** Upgrade instance type for more CPU/RAM
- **Horizontal:** Add more instances (requires session storage configuration)

For horizontal scaling, consider:
- Using PostgreSQL for session storage
- Configuring Redis for caching
- Using object storage (S3) for media files
