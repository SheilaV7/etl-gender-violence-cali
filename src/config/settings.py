from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("SUPABASE_DB_URL")
