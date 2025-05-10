# myapp/supabase_client.py
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://xyzcompany.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-key")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
