from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from services.encryption import encrypt_data, decrypt_data
from services.local_store import get_user, upsert_user, get_projects, add_project as local_add_project

# Lazy connection check: on first failure supabase is disabled for the session
_supabase_ok = True
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        _supabase_ok = False
        print(f"Failed to initialize Supabase client: {e}")

def _supabase_enabled():
    return supabase is not None and _supabase_ok

def _disable_supabase():
    global _supabase_ok
    _supabase_ok = False

def _check(response, msg="Supabase error"):
    if hasattr(response, "status_code") and response.status_code >= 400:
        raise Exception(f"{msg}: HTTP {response.status_code}")

def _defaults(user_id):
    return {
        "user_id": user_id,
        "language": "en",
        "auto_seo": True,
    }

async def get_user_language(user_id: int) -> str:
    if _supabase_enabled():
        try:
            response = supabase.table("users").select("language").eq("user_id", user_id).execute()
            if response.data:
                return response.data[0]["language"]
        except Exception as e:
            print(f"Supabase error, disabling: {e}")
            _disable_supabase()
    user = get_user(user_id)
    if user:
        return user.get("language", "en")
    return "en"

async def set_user_language(user_id: int, language: str):
    if _supabase_enabled():
        try:
            r = supabase.table("users").select("user_id").eq("user_id", user_id).execute()
            _check(r)
            if r.data:
                r2 = supabase.table("users").update({"language": language}).eq("user_id", user_id).execute()
                _check(r2)
            else:
                r2 = supabase.table("users").insert({"user_id": user_id, "language": language}).execute()
                _check(r2)
            return
        except Exception as e:
            print(f"Supabase error, disabling: {e}")
            _disable_supabase()
    upsert_user(user_id, {"language": language})

async def save_project(user_id: int, project_name: str, live_url: str, seo_score: int):
    if _supabase_enabled():
        try:
            r = supabase.table("projects").insert({
                "user_id": user_id,
                "project_name": project_name,
                "live_url": live_url,
                "seo_score": seo_score
            }).execute()
            _check(r, "Save project")
            return
        except Exception as e:
            print(f"Supabase error, disabling: {e}")
            _disable_supabase()
    local_add_project(user_id, project_name, live_url, seo_score)

async def get_user_projects(user_id: int):
    if _supabase_enabled():
        try:
            response = supabase.table("projects").select("*").eq("user_id", user_id).execute()
            return response.data
        except Exception as e:
            print(f"Supabase error, disabling: {e}")
            _disable_supabase()
    return get_projects(user_id) or []

async def get_user_settings(user_id: int) -> dict:
    if _supabase_enabled():
        try:
            response = supabase.table("users").select("*").eq("user_id", user_id).execute()
            if response.data:
                user = response.data[0]
                if user.get("ai_api_key_enc"):
                    user["ai_api_key"] = decrypt_data(user["ai_api_key_enc"])
                if user.get("db_credentials_enc"):
                    user["db_credentials"] = decrypt_data(user["db_credentials_enc"])
                if user.get("hosting_token_enc"):
                    user["hosting_token"] = decrypt_data(user["hosting_token_enc"])
                return user
            supabase.table("users").insert(_defaults(user_id)).execute()
        except Exception as e:
            print(f"Supabase error, disabling: {e}")
            _disable_supabase()
    user = get_user(user_id)
    if user:
        if user.get("ai_api_key_enc"):
            user["ai_api_key"] = decrypt_data(user["ai_api_key_enc"])
        if user.get("db_credentials_enc"):
            user["db_credentials"] = decrypt_data(user["db_credentials_enc"])
        if user.get("hosting_token_enc"):
            user["hosting_token"] = decrypt_data(user["hosting_token_enc"])
        return {**_defaults(user_id), **user}
    return _defaults(user_id)

async def update_user_settings(user_id: int, updates: dict):
    data_to_save = updates.copy()
    if "ai_api_key" in data_to_save:
        val = data_to_save.pop("ai_api_key")
        data_to_save["ai_api_key_enc"] = encrypt_data(val) if val else None
    if "db_credentials" in data_to_save:
        val = data_to_save.pop("db_credentials")
        data_to_save["db_credentials_enc"] = encrypt_data(val) if val else None
    if "hosting_token" in data_to_save:
        val = data_to_save.pop("hosting_token")
        data_to_save["hosting_token_enc"] = encrypt_data(val) if val else None

    if _supabase_enabled():
        try:
            r = supabase.table("users").select("user_id").eq("user_id", user_id).execute()
            _check(r)
            if r.data:
                r2 = supabase.table("users").update(data_to_save).eq("user_id", user_id).execute()
                _check(r2)
            else:
                data_to_save["user_id"] = user_id
                r2 = supabase.table("users").insert(data_to_save).execute()
                _check(r2)
            return
        except Exception as e:
            print(f"Supabase error, disabling: {e}")
            _disable_supabase()
    upsert_user(user_id, data_to_save)
