import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing required Supabase environment variables")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def apply_migrations():
    """Apply database migrations"""
    print("\nStarting database migrations...")
    
    # Get init.sql file
    init_sql_path = Path(__file__).parent.parent / "migrations" / "init.sql"
    
    try:
        # Read migration file
        print(f"\nReading init.sql...")
        with open(init_sql_path, 'r') as f:
            sql = f.read()
        
        # Execute SQL directly using Supabase's REST API
        print("\nExecuting SQL...")
        response = supabase.rpc('exec_sql', {'query': sql}).execute()
        print(f"Migration response: {response}")
        
        print("\nMigration completed successfully!")
        
    except Exception as e:
        print(f"\nError applying migration:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        raise

if __name__ == "__main__":
    apply_migrations() 