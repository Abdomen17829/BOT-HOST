import aiohttp
from supabase import create_client
from motor.motor_asyncio import AsyncIOMotorClient
import json

async def ping_supabase(url: str, key: str) -> bool:
    try:
        headers = {"apikey": key, "Authorization": f"Bearer {key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}/rest/v1/", headers=headers) as response:
                return response.status in [200, 404]
    except:
        return False

async def ping_mongodb(uri: str) -> bool:
    try:
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=2000)
        await client.admin.command('ping')
        return True
    except:
        return False

async def ping_firebase(json_str: str) -> bool:
    try:
        data = json.loads(json_str)
        if "project_id" in data and "private_key" in data:
            return True
        return False
    except:
        return False

async def save_project_to_dynamic_db(db_provider: str, creds: str, user_id: int, project_name: str, live_url: str, seo_score: int):
    try:
        if db_provider == "Supabase":
            c = json.loads(creds)
            client = create_client(c['url'], c['key'])
            client.table("projects").insert({
                "user_id": user_id,
                "project_name": project_name,
                "live_url": live_url,
                "seo_score": seo_score
            }).execute()
        elif db_provider == "MongoDB":
            client = AsyncIOMotorClient(creds)
            db = client.get_database("telegram_bot_db")
            await db.projects.insert_one({
                "user_id": user_id,
                "project_name": project_name,
                "live_url": live_url,
                "seo_score": seo_score
            })
        elif db_provider == "Firebase":
            import firebase_admin
            from firebase_admin import credentials, firestore
            app_name = f"app_{user_id}"
            try:
                app = firebase_admin.get_app(app_name)
            except ValueError:
                cred_dict = json.loads(creds)
                cred = credentials.Certificate(cred_dict)
                app = firebase_admin.initialize_app(cred, name=app_name)
                
            db = firestore.client(app=app)
            db.collection('projects').add({
                "user_id": user_id,
                "project_name": project_name,
                "live_url": live_url,
                "seo_score": seo_score
            })
    except Exception as e:
        print(f"Error saving to dynamic DB: {e}")


async def ping_database(provider: str, creds_raw: str) -> bool:
    """Unified ping dispatcher — routes to the correct provider."""
    try:
        if provider == "Supabase":
            data = json.loads(creds_raw)
            return await ping_supabase(data.get("url", ""), data.get("key", ""))
        elif provider == "MongoDB":
            return await ping_mongodb(creds_raw)
        elif provider == "Firebase":
            return await ping_firebase(creds_raw)
        return False
    except Exception as e:
        print(f"ping_database error: {e}")
        return False
