# Deployment Guide

This project can be deployed to production after real infrastructure and real environment values are configured.

## Railway

This repository now includes [railway.toml](/C:/Users/ADMIN/Downloads/lms_django_project/lms_project/railway.toml) for Railway config-as-code:

- build runs `python manage.py collectstatic --noinput`
- pre-deploy runs `python manage.py migrate --noinput`
- start runs Gunicorn
- healthcheck uses `/health/`

Railway-specific notes:

- Railway provides `PORT` automatically, which Gunicorn already uses.
- If Railway provides `RAILWAY_PUBLIC_DOMAIN`, the app now auto-adds it to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
- If Railway provides `DATABASE_URL`, the app now parses it automatically.

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

Install a production database driver as needed:

```bash
# PostgreSQL
pip install psycopg2-binary

# or MySQL / MariaDB
pip install mysqlclient
```

## 2. Configure environment

Use `.env.production.example` as the starting point.

Minimum production expectations:

```env
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
USE_WHITENOISE=True
ENABLE_PUBLIC_REGISTRATION=False
ENABLE_SEED_TOOLS=False
ENABLE_DEMO_DATA=False
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

Database example for PostgreSQL:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
```

## 3. Prepare the app

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py check --deploy
```

`python manage.py check --deploy` now fails if production still has:

- public self-registration enabled
- seed tools enabled
- demo data mode enabled
- console email backend enabled

## 4. Start the server

Use Gunicorn:

```bash
gunicorn config.wsgi:application -c gunicorn.conf.py
```

The included `Procfile` can be used on platforms that support it.

## 5. Reverse proxy and HTTPS

Put the app behind HTTPS with Nginx, Caddy, Apache, or a cloud platform proxy. If SSL terminates at the proxy, make sure `SECURE_PROXY_SSL_HEADER` matches the forwarded header.

## 6. Static and media

- Static files are served by WhiteNoise when `USE_WHITENOISE=True`.
- Media uploads should be served by the reverse proxy or object storage.

## 7. Final checklist

- `DEBUG=False`
- strong `SECRET_KEY`
- real domain values in `ALLOWED_HOSTS`
- real HTTPS values in `CSRF_TRUSTED_ORIGINS`
- production database configured
- production SMTP configured
- demo flags disabled
- `python manage.py check --deploy` passes
- backups exist for database and media
- production data does not include demo accounts or seeded test records
