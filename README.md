# LibraMS

Library management system built with Django 4.2.

## Stack

- Python 3.10+
- Django 4.2
- SQLite for local development
- MySQL or PostgreSQL for production
- Django templates, custom CSS, Chart.js

## Local Development

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` if you want custom local settings.
4. Run the development setup:

```bash
python setup.py
```

5. Start the app:

```bash
python manage.py runserver
```

6. Open:

```text
http://127.0.0.1:8000/login/
```

When demo mode is enabled, setup creates the demo login `admin` / `admin123`.

## Production

Use `.env.production.example` as the base for production configuration.

For Railway specifically, this repo includes [railway.toml](/C:/Users/ADMIN/Downloads/lms_django_project/lms_project/railway.toml), a `/health/` endpoint, and automatic support for Railway `DATABASE_URL` and `RAILWAY_PUBLIC_DOMAIN`.

Required production expectations:

- `DEBUG=False`
- `ENABLE_PUBLIC_REGISTRATION=False`
- `ENABLE_SEED_TOOLS=False`
- `ENABLE_DEMO_DATA=False`
- real `SECRET_KEY`
- real `ALLOWED_HOSTS`
- real `CSRF_TRUSTED_ORIGINS`
- real SMTP-backed `EMAIL_BACKEND`
- real production database

Run the deploy checks before launch:

```bash
python manage.py check --deploy
```

The deploy checks now fail if production still has public registration, seed tools, demo data mode, or the console email backend enabled.

Full deployment instructions are in [DEPLOYMENT.md](/C:/Users/ADMIN/Downloads/lms_django_project/lms_project/DEPLOYMENT.md).

## Common Commands

```bash
python manage.py test
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py update_fines
python manage.py send_reminders
python manage.py seed_data
python manage.py check --deploy
```

## Notes

- `seed_data` and demo credentials are for development only.
- `setup.py` respects `ENABLE_DEMO_DATA`; if demo mode is off, it tells you to create a real admin user instead.
- Static files are prepared for WhiteNoise in production.
