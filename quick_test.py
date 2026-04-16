import os
from dotenv import load_dotenv
load_dotenv()

from apps.library.supabase_client import supabase

print("Testing Supabase connection...")
result = supabase().table('library_book').select('title, author').limit(3).execute()
print(f"✅ Connection works! Found {len(result.data)} books:")
for book in result.data:
    print(f"  - {book['title']} by {book['author']}")
