#!/bin/bash
# Supabase Setup Script for Django LMS

echo "==================================="
echo "Supabase Setup for Django LMS"
echo "==================================="

# Step 1: Install Supabase Python client
echo ""
echo "Step 1: Installing Supabase Python client..."
pip install supabase

# Step 2: Load environment variables
echo ""
echo "Step 2: Loading environment variables..."
if [ -f .env.supabase ]; then
    export $(cat .env.supabase | grep -v '^#' | xargs)
    echo "✓ Environment variables loaded from .env.supabase"
else
    echo "⚠ Warning: .env.supabase file not found"
fi

# Step 3: Test Supabase connection
echo ""
echo "Step 3: Testing Supabase connection..."
python -c "
from apps.library.supabase_client import supabase
try:
    result = supabase().table('library_book').select('count').execute()
    print('✓ Successfully connected to Supabase!')
    print(f'  Database has {len(result.data)} books')
except Exception as e:
    print(f'✗ Connection failed: {e}')
"

# Step 4: Optional - Sync existing data
echo ""
echo "Step 4: Sync existing data to Supabase? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Syncing data to Supabase..."
    python manage.py sync_to_supabase
    echo "✓ Data sync complete"
else
    echo "Skipping data sync"
fi

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Update your Django settings (see config/settings/supabase_config.py)"
echo "2. Read SUPABASE_SETUP.md for detailed integration guide"
echo "3. Access your Supabase dashboard:"
echo "   https://supabase.com/dashboard/project/otnctayrocscihsmhhcs"
echo ""
