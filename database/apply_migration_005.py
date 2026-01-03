"""
Apply Migration 005: Fix Snapshot Function Security
Adds SECURITY DEFINER to snapshot creation functions to bypass RLS
"""

import sys
from pathlib import Path

# Add backend to path to import supabase client
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from supabase import create_client
from config import settings

print("=" * 80)
print("MIGRATION 005: Fix Snapshot Function Security")
print("=" * 80)
print()

# Initialize Supabase with service role key (admin access)
# NOTE: This uses SUPABASE_ANON_KEY which might not have permission to modify functions
# You may need to run the SQL directly in the Supabase dashboard SQL editor
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

# Read the migration file
migration_path = Path(__file__).parent / "migrations" / "005_fix_snapshot_function_security.sql"

with open(migration_path, 'r', encoding='utf-8') as f:
    migration_sql = f.read()

print("Migration SQL loaded from:", migration_path)
print()
print("=" * 80)
print("IMPORTANT: This script may not have permissions to modify database functions.")
print("If you get permission errors, please:")
print("1. Go to your Supabase Dashboard")
print("2. Navigate to SQL Editor")
print("3. Copy the contents of: database/migrations/005_fix_snapshot_function_security.sql")
print("4. Paste and run it in the SQL Editor")
print("=" * 80)
print()

try:
    # Attempt to execute the migration
    # Note: Supabase Python client doesn't have direct SQL execution
    # This is a placeholder - you'll need to run the SQL manually

    print("Attempting to apply migration...")
    print()
    print("⚠️  WARNING: The Supabase Python client doesn't support executing raw SQL.")
    print("Please apply this migration manually using one of these methods:")
    print()
    print("METHOD 1: Supabase Dashboard (Recommended)")
    print("  1. Go to: https://supabase.com/dashboard")
    print("  2. Open your project")
    print("  3. Navigate to SQL Editor")
    print("  4. Create a new query")
    print("  5. Copy/paste the contents of:")
    print(f"     {migration_path}")
    print("  6. Click 'Run'")
    print()
    print("METHOD 2: psql command line")
    print("  If you have your database connection string:")
    print(f"  psql 'your-connection-string' < {migration_path}")
    print()

    # Print the SQL for convenience
    print("=" * 80)
    print("SQL TO EXECUTE:")
    print("=" * 80)
    print(migration_sql)
    print("=" * 80)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
