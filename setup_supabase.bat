@echo off
REM Supabase Setup Script for Django LMS (Windows)

echo ===================================
echo Supabase Setup for Django LMS
echo ===================================

REM Step 1: Install Supabase Python client
echo.
echo Step 1: Installing Supabase Python client...
pip install supabase

REM Step 2: Load environment variables
echo.
echo Step 2: Environment variables...
if exist .env.supabase (
    echo Environment variables are in .env.supabase
    echo Please load them manually or add to your system
) else (
    echo Warning: .env.supabase file not found
)

REM Step 3: Test Supabase connection
echo.
echo Step 3: Testing Supabase connection...
python -c "from apps.library.supabase_client import supabase; result = supabase().table('library_book').select('count').execute(); print('Successfully connected to Supabase!')"

REM Step 4: Optional - Sync existing data
echo.
echo Step 4: Sync existing data to Supabase? (y/n)
set /p response=
if /i "%response%"=="y" (
    echo Syncing data to Supabase...
    python manage.py sync_to_supabase
    echo Data sync complete
) else (
    echo Skipping data sync
)

echo.
echo ===================================
echo Setup Complete!
echo ===================================
echo.
echo Next steps:
echo 1. Update your Django settings (see config/settings/supabase_config.py)
echo 2. Read SUPABASE_SETUP.md for detailed integration guide
echo 3. Access your Supabase dashboard:
echo    https://supabase.com/dashboard/project/otnctayrocscihsmhhcs
echo.
pause
