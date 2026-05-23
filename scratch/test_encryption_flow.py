import asyncio
import os
import sys
import json
import shutil

# Add workspace root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ensure we use local fallback by disabling supabase configuration temporarily
import services.database as db
db._supabase_ok = False
db.supabase = None

from services.database import get_user_settings, update_user_settings
from services.local_store import DATA_DIR, USERS_FILE
from services.encryption import decrypt_data

async def run_test():
    user_id = 9999999
    
    # Clean up previous test data if any
    if os.path.exists(USERS_FILE):
        users_data = {}
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                users_data = json.load(f)
            except:
                pass
        if str(user_id) in users_data:
            del users_data[str(user_id)]
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(users_data, f, indent=2)

    # 1. Prepare raw inputs
    raw_ai_key = "sk-or-dummy-api-key-12345"
    raw_host_token = "netlify-dummy-token-abcde"
    raw_db_creds = '{"url": "https://dummy.supabase.co", "key": "dummy-key"}'

    # 2. Call update_user_settings (simulating settings form callback flow)
    print("Saving settings...")
    await update_user_settings(user_id, {
        "ai_provider": "OpenRouter",
        "ai_api_key": raw_ai_key,
        "ai_model": "openai/gpt-4-turbo",
        "db_provider": "Supabase",
        "db_credentials": raw_db_creds,
        "hosting_provider": "Netlify",
        "hosting_token": raw_host_token
    })

    # 3. Read directly from local JSON to verify it is encrypted (single encryption)
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        user_record = data[str(user_id)]
        
        # Keys in database are stored with _enc suffix
        ai_enc = user_record.get("ai_api_key_enc")
        host_enc = user_record.get("hosting_token_enc")
        db_enc = user_record.get("db_credentials_enc")

        assert ai_enc != raw_ai_key, "AI Key was not encrypted!"
        assert host_enc != raw_host_token, "Hosting token was not encrypted!"
        assert db_enc != raw_db_creds, "DB credentials were not encrypted!"

        # Let's decrypt once to see if it becomes raw key (verifies only single encryption)
        decrypted_ai = decrypt_data(ai_enc)
        decrypted_host = decrypt_data(host_enc)
        decrypted_db = decrypt_data(db_enc)

        assert decrypted_ai == raw_ai_key, f"AI Key encryption incorrect. Expected raw but got: {decrypted_ai}"
        assert decrypted_host == raw_host_token, "Hosting token encryption incorrect."
        assert decrypted_db == raw_db_creds, "DB credentials encryption incorrect."
        
        print("[OK] Verified data is encrypted exactly once in storage.")
    
    # 4. Call get_user_settings to verify automatic decryption works on retrieval
    retrieved = await get_user_settings(user_id)
    
    assert retrieved.get("ai_api_key") == raw_ai_key, f"Retrieved AI Key mismatch! Got: {retrieved.get('ai_api_key')}"
    assert retrieved.get("hosting_token") == raw_host_token, f"Retrieved Hosting Token mismatch! Got: {retrieved.get('hosting_token')}"
    assert retrieved.get("db_credentials") == raw_db_creds, f"Retrieved DB Credentials mismatch! Got: {retrieved.get('db_credentials')}"
    
    print("[OK] Verified get_user_settings successfully decrypts keys on local fallback.")
    
    # Cleanup
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users_data = json.load(f)
    if str(user_id) in users_data:
        del users_data[str(user_id)]
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=2)
    print("Cleanup successful.")

if __name__ == "__main__":
    asyncio.run(run_test())
