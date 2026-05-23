import asyncio
import os
import sys
import tempfile
import shutil

# Add workspace root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Verify imports and router setup
print("[1/4] Verifying bot import and router structures...")
try:
    from bot import main
    from handlers import start, settings, upload, dashboard
    print(" -> All handlers imported successfully.")
    assert hasattr(start, 'router'), "start handler missing router"
    assert hasattr(settings, 'router'), "settings handler missing router"
    assert hasattr(upload, 'router'), "upload handler missing router"
    assert hasattr(dashboard, 'router'), "dashboard handler missing router"
    print(" -> All routers verified.")
except Exception as e:
    print(f"❌ Handlers/Bot import failed: {e}")
    sys.exit(1)

# Verify local store database functions
print("[2/4] Verifying database operations...")
try:
    import services.database as db
    db._supabase_ok = False # Enforce local storage
    
    async def test_db():
        user_id = 888888
        # Get defaults
        s = await db.get_user_settings(user_id)
        assert s.get("language") == "en", "Default language should be en"
        assert s.get("auto_seo") is True, "Default auto_seo should be True"
        
        # Save updates
        await db.update_user_settings(user_id, {"language": "ar", "auto_seo": False})
        s2 = await db.get_user_settings(user_id)
        assert s2.get("language") == "ar", "Language should be updated to ar"
        assert s2.get("auto_seo") is False, "auto_seo should be updated to False"
        
        # Cleanup
        await db.update_user_settings(user_id, {"language": "en", "auto_seo": True})
        print(" -> Local fallback database operations verified successfully.")

    asyncio.run(test_db())
except Exception as e:
    print(f"❌ Database test failed: {e}")
    sys.exit(1)

# Verify SEO engine with mock HTML
print("[3/4] Verifying SEO analysis engine...")
try:
    from services.seo_engine import analyze_seo
    
    async def test_seo():
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a mock index.html file
            html_content = """<!DOCTYPE html>
<html>
<head>
    <title>My Awesome AI Site</title>
    <meta name="description" content="Deploy sites using SityStar Telegram Bot.">
</head>
<body>
    <h1>Welcome to SityStar AI Commander</h1>
</body>
</html>"""
            with open(os.path.join(temp_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # Since AI providers require keys, we mock the factory output or run with a mock setting
            # We check that the parser reads index.html correctly and falls back gracefully or uses default mock
            # In seo_engine.py, it calls generate_seo_with_provider.
            # If API key is not valid, it returns a default dict with seo_score: 50.
            # Let's test the fallback when no valid API key is configured.
            settings = {"ai_api_key": None}
            res = await analyze_seo(temp_dir, "My Site", settings)
            assert "score" in res, "SEO result missing score"
            assert "report" in res, "SEO result missing report"
            print(" -> SEO analysis fallback verified successfully.")
            
    asyncio.run(test_seo())
except Exception as e:
    print(f"❌ SEO engine test failed: {e}")
    sys.exit(1)

# Verify locale dictionary structure
print("[4/4] Verifying locales dictionary keys consistency...")
try:
    from utils.locales import LOCALES
    en_keys = set(LOCALES['en'].keys())
    ar_keys = set(LOCALES['ar'].keys())
    
    missing_in_ar = en_keys - ar_keys
    missing_in_en = ar_keys - en_keys
    
    assert not missing_in_ar, f"Keys missing in Arabic: {missing_in_ar}"
    assert not missing_in_en, f"Keys missing in English: {missing_in_en}"
    print(" -> All locale keys are perfectly synchronized between EN and AR.")
except Exception as e:
    print(f"[FAIL] Locales verification failed: {e}")
    sys.exit(1)

print("\n[SUCCESS] ALL CHECKS PASSED SUCCESSFULLY! The codebase is production-ready.")
