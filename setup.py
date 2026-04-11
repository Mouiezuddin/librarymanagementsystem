#!/usr/bin/env python
"""
LibraMS — One-click Setup Script
Run once after cloning / extracting the project:

    python setup.py

What it does:
  1. Applies all database migrations
  2. Seeds demo data when demo mode is enabled
  3. Seeds 20 sample books, 11 members, 10 categories
  4. Creates 8 sample issue records (some overdue) for testing

After running, start the server with:
    python manage.py runserver
Then visit: http://127.0.0.1:8000/login/
"""

import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "=" * 56)
print("      LibraMS  -  Library Management System")
print("  BCA Project 2023-2026 | Smt Kumudben Darbar College")
print("=" * 56)

import django
django.setup()

from django.conf import settings
from django.core.management import call_command

print("\n[1/2] Applying database migrations...")
call_command('migrate', verbosity=0)
print("      v Done")

print("\n[2/2] Seeding sample data...")
call_command('seed_data')

print("=" * 56)
print("  [OK] Setup complete!")
print("=" * 56)
print()
print("  Start the development server:")
print("  $ python manage.py runserver")
print()
print("  Open in your browser:")
print("  http://127.0.0.1:8000/login/")
print()
if settings.ENABLE_DEMO_DATA:
    print("  Demo login credentials:")
    print("  Username : admin")
    print("  Password : admin123")
    print()
else:
    print("  Demo credentials are disabled in this environment.")
    print("  Create an admin account with:")
    print("  $ python manage.py createsuperuser")
    print()
print("  Useful management commands:")
print("  $ python manage.py update_fines      - recalculate all overdue fines")
print("  $ python manage.py send_reminders    - create due-date notifications")
print("  $ python manage.py seed_data --clear - wipe and re-seed sample data")
print("  $ python manage.py createsuperuser   - add another admin user")
print("=" * 56 + "\n")
