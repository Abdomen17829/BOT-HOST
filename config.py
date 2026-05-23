import os
from dotenv import load_dotenv, set_key
from cryptography.fernet import Fernet

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
NETLIFY_ACCESS_TOKEN = os.getenv("NETLIFY_ACCESS_TOKEN", "")
VERCEL_ACCESS_TOKEN = os.getenv("VERCEL_ACCESS_TOKEN", "")

# Handle Encryption Key dynamically
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    if os.path.exists(env_path):
        set_key(env_path, "ENCRYPTION_KEY", ENCRYPTION_KEY)
    else:
        with open(env_path, "w") as f:
            f.write(f"ENCRYPTION_KEY={ENCRYPTION_KEY}\n")
    print("New ENCRYPTION_KEY generated and saved to .env")
