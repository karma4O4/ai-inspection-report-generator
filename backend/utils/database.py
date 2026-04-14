import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    # Set standard defaults to avoid crashing during module load if env file isn't filled yet
    SUPABASE_URL = "https://placeholder-project.supabase.co"
    SUPABASE_KEY = "placeholder-key"

# Create the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db():
    """Dependency helper to get the database client."""
    return supabase
