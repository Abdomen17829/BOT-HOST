import os
import zipfile
import tarfile
import aiohttp
import shutil
import time
import patoolib
from aiogram import Router, types, F
from services.database import get_user_settings, save_project
from services.dynamic_db import save_project_to_dynamic_db
from services.seo_engine import analyze_seo
from services.dynamic_hosting import deploy_to_netlify, deploy_to_vercel
from utils.locales import LOCALES
from config import TELEGRAM_BOT_TOKEN, NETLIFY_ACCESS_TOKEN, VERCEL_ACCESS_TOKEN

router = Router()


async def process_upload_pipeline(
    message: types.Message,
    project_name: str,
    clean_zip_path: str,
    extract_dir: str,
    settings: dict,
):
    lang = settings.get("language", "en")
    texts = LOCALES[lang]
    status_msg = await message.answer(texts['processing'])
    original_zip_path = clean_zip_path

    try:
        host_prov = settings.get("hosting_provider") or "Netlify"
        user_token = settings.get("hosting_token")
        default_token = VERCEL_ACCESS_TOKEN if host_prov == "Vercel" else NETLIFY_ACCESS_TOKEN
        host_token = user_token or default_token
        live_url = None

        print(f"[Deploy] provider={host_prov}, user_token={bool(user_token)}, fallback={bool(default_token)}, zip={original_zip_path}")
        await status_msg.edit_text(texts['deploying'].format(provider=host_prov))
        if host_prov == "Vercel":
            root_dir = find_root_directory(extract_dir)
            live_url = await deploy_to_vercel(root_dir, host_token, project_name)
        else:
            live_url = await deploy_to_netlify(original_zip_path, host_token)
        print(f"[Deploy] result: {live_url}")

        if not live_url:
            raise Exception(texts.get('error_no_token', 'Deployment failed. Check your hosting token.'))

        # ── STEP 2: SEO Analysis ─────────────────────────────────────────
        seo_score = 50
        auto_seo = settings.get("auto_seo", True)
        seo_report = ""

        if auto_seo:
            print("[SEO] Starting analysis...")
            await status_msg.edit_text(texts['seo_gen'])
            root_dir2 = find_root_directory(extract_dir)
            seo_result = await analyze_seo(root_dir2, project_name, settings)
            seo_score = seo_result.get("score", 50)
            seo_report = seo_result.get("report", "")
            print(f"[SEO] Done: score={seo_score}")

        # ── STEP 3: Save project ─────────────────────────────────────────
        print(f"[Save] project={project_name}, url={live_url}")
        await save_project(message.from_user.id, project_name, live_url, seo_score)

        db_prov = settings.get("db_provider")
        db_creds = settings.get("db_credentials")
        if db_prov and db_creds:
            await save_project_to_dynamic_db(
                db_prov, db_creds, message.from_user.id, project_name, live_url, seo_score
            )

        # ── STEP 4: Send response ────────────────────────────────────────
        success_text = texts['success'].format(url=live_url, name=project_name, score=seo_score)
        await status_msg.edit_text(success_text, disable_web_page_preview=True, parse_mode="Markdown")
        print("[Done] Success")

        if seo_report and "No AI key" not in seo_report:
            await message.answer(seo_report, parse_mode="Markdown")

    except Exception as e:
        err_msg = f"[{type(e).__name__}] {e}"
        print(f"[Error] {err_msg}")
        await status_msg.edit_text(texts['error_general'].format(error=err_msg), parse_mode="Markdown")


async def download_file(file_id: str, bot, destination: str):
    file = await bot.get_file(file_id)
    url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file.file_path}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Download failed: HTTP {response.status}")
            with open(destination, 'wb') as f:
                f.write(await response.read())


def find_root_directory(extract_dir: str) -> str:
    """Finds the deepest directory that contains index.html."""
    for root, dirs, files in os.walk(extract_dir):
        if "index.html" in files:
            return root
    return extract_dir


# ── Helper: extract any archive and re-zip with clean paths ─────────────
async def prepare_zip(original_path: str, ext: str, extract_dir: str, base_dir: str) -> str:
    if ext == '.html':
        os.makedirs(extract_dir, exist_ok=True)
        shutil.copy(original_path, os.path.join(extract_dir, "index.html"))
    elif ext == '.zip':
        with zipfile.ZipFile(original_path, 'r') as zf:
            zf.extractall(extract_dir)
    else:
        patoolib.extract_archive(original_path, outdir=extract_dir, interactive=False)

    # Unpack nested zip if extracted gave us a single zip
    for _ in range(3):
        nested = []
        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f.endswith('.zip'):
                    nested.append(os.path.join(root, f))
        if not nested:
            break
        for nz in nested:
            nest_dir = os.path.join(os.path.dirname(nz), os.path.splitext(os.path.basename(nz))[0])
            os.makedirs(nest_dir, exist_ok=True)
            with zipfile.ZipFile(nz, 'r') as zf:
                zf.extractall(nest_dir)
            os.remove(nz)

    # Gather all files with relative paths
    all_files = []
    for root, _, files in os.walk(extract_dir):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, extract_dir)
            if f.endswith('.zip'):
                continue
            all_files.append((full, rel))

    # Strip common single top-level dir (GitHub pattern: repo-master/{files})
    top_items = [x for x in os.listdir(extract_dir) if x != '__MACOSX']
    strip_top = len(top_items) == 1 and os.path.isdir(os.path.join(extract_dir, top_items[0]))

    # Rename single .html to index.html for Netlify/Vercel
    html_files = [a for a in all_files if a[1].endswith('.html') and not a[1].endswith('index.html')]
    has_index = any(a[1].endswith('index.html') for a in all_files)

    final_zip = os.path.join(base_dir, "final_deploy.zip")
    with zipfile.ZipFile(final_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for full, rel in all_files:
            parts = rel.split(os.sep)
            arcname = os.path.join(*parts[1:]) if strip_top else rel
            if not has_index and len(html_files) == 1 and rel == html_files[0][1]:
                arcname = "index.html"
            zf.write(full, arcname)
        # Force Netlify to serve HTML with correct content-type
        zf.writestr("_headers", "/*.html\n  Content-Type: text/html\n")

    with zipfile.ZipFile(final_zip, 'r') as test:
        if test.testzip() is not None:
            raise Exception("Generated zip is corrupted")

    print(f"Zip prepared: {len(all_files)} files, size={os.path.getsize(final_zip)}, strip_top={strip_top}")
    return final_zip


@router.message(F.document)
async def handle_document(message: types.Message):
    user_id = message.from_user.id
    settings = await get_user_settings(user_id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]

    file_name = message.document.file_name
    fname_lower = file_name.lower()
    valid_exts = ['.zip', '.rar', '.7z', '.tar.gz', '.html']
    matched_ext = next((e for e in valid_exts if fname_lower.endswith(e)), None)

    if not matched_ext:
        await message.answer(texts['error_format'])
        return

    timestamp = int(time.time())
    base_dir = os.path.join(os.getcwd(), f"tmp_{user_id}_{timestamp}")
    os.makedirs(base_dir, exist_ok=True)
    original_path = os.path.join(base_dir, f"upload{matched_ext}")
    extract_dir = os.path.join(base_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    try:
        print(f"[Upload] Starting for {file_name} (user={user_id})")
        status_msg = await message.answer(texts['extracting'])
        await download_file(message.document.file_id, message.bot, original_path)
        print(f"[Upload] Downloaded to {original_path}")

        clean_zip = await prepare_zip(original_path, matched_ext, extract_dir, base_dir)
        print(f"[Upload] Clean zip: {clean_zip}")
        for r, _, fs in os.walk(extract_dir):
            for f in fs:
                print(f"  File: {os.path.join(r, f)}")

        project_name = file_name
        for ext in valid_exts:
            project_name = project_name.replace(ext, "").replace(ext.upper(), "")
        project_name = project_name.strip("_- ")

        await status_msg.delete()
        await process_upload_pipeline(message, project_name, clean_zip, extract_dir, settings)

    except Exception as e:
        err_msg = f"[{type(e).__name__}] {e}"
        print(f"[Upload] Error: {err_msg}")
        await message.answer(texts['error_general'].format(error=err_msg))
    finally:
        shutil.rmtree(base_dir, ignore_errors=True)
        print(f"[Upload] Cleaned up {base_dir}")


@router.message(F.text.regexp(r'https://github\.com/[^\s]+'))
async def handle_github(message: types.Message):
    user_id = message.from_user.id
    settings = await get_user_settings(user_id)
    lang = settings.get("language", "en")
    texts = LOCALES[lang]

    repo_url = message.text.strip().rstrip('/')
    status_msg = await message.answer(texts['processing'])

    timestamp = int(time.time())
    base_dir = os.path.join(os.getcwd(), f"tmp_{user_id}_{timestamp}")
    os.makedirs(base_dir, exist_ok=True)
    raw_zip = os.path.join(base_dir, "repo_raw.zip")
    extract_dir = os.path.join(base_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    try:
        downloaded = False
        async with aiohttp.ClientSession() as session:
            for branch in ["main", "master"]:
                zip_url = f"{repo_url}/archive/refs/heads/{branch}.zip"
                async with session.get(zip_url) as resp:
                    if resp.status == 200:
                        with open(raw_zip, 'wb') as f:
                            f.write(await resp.read())
                        downloaded = True
                        break

        if not downloaded:
            raise Exception("Could not download repository. Make sure the repo is public.")

        await status_msg.edit_text(texts['extracting'])
        clean_zip = await prepare_zip(raw_zip, '.zip', extract_dir, base_dir)
        project_name = repo_url.split('/')[-1]

        await status_msg.delete()
        await process_upload_pipeline(message, project_name, clean_zip, extract_dir, settings)

    except Exception as e:
        await status_msg.edit_text(texts['error_general'].format(error=str(e)))
    finally:
        shutil.rmtree(base_dir, ignore_errors=True)
