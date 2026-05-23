import aiohttp
import ssl
import os
import hashlib
import json

# Windows SSL compat: create_default_context may fail on some Win builds
try:
    _SSL_CTX = ssl.create_default_context()
except Exception:
    _SSL_CTX = False


# ─── NETLIFY DEPLOY (Direct zip upload) ──────────────────────────────────────
async def deploy_to_netlify(zip_path: str, token: str) -> str:
    if not token or not zip_path:
        print("Netlify: missing token or zip path")
        return None

    try:
        # Read zip with error context
        try:
            with open(zip_path, 'rb') as f:
                zip_data = f.read()
        except Exception as e:
            print(f"Netlify: cannot read zip ({zip_path}): {e}")
            return None

        if not zip_data:
            print("Netlify: empty zip")
            return None

        import zipfile as _zf
        with _zf.ZipFile(zip_path, 'r') as _z:
            for _n in _z.namelist():
                print(f"  Zip content: {_n}")
        print(f"  Total files in zip: {len(_z.namelist())}")

        connector = aiohttp.TCPConnector(ssl=_SSL_CTX)
        async with aiohttp.ClientSession(connector=connector) as session:
            headers_create = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            async with session.post(
                "https://api.netlify.com/api/v1/sites",
                headers=headers_create,
                json={}
            ) as resp_create:
                body_create = await resp_create.text()
                if resp_create.status not in [200, 201]:
                    print(f"Netlify site creation failed ({resp_create.status}): {body_create[:200]}")
                    return None
                site_data = json.loads(body_create)
                site_id = site_data.get("id")
                subdomain = site_data.get("subdomain")
                url = f"https://{subdomain}.netlify.app" if subdomain else site_data.get("url")

            if not site_id:
                print("Netlify: site created but site_id missing")
                return None

            headers_deploy = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/zip"
            }
            async with session.post(
                f"https://api.netlify.com/api/v1/sites/{site_id}/deploys",
                headers=headers_deploy,
                data=zip_data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp_deploy:
                body_deploy = await resp_deploy.text()
                if resp_deploy.status not in [200, 201]:
                    print(f"Netlify ZIP upload failed ({resp_deploy.status}): {body_deploy[:200]}")
                    return None

            print(f"Netlify deployed successfully: {url}")
            return url

    except aiohttp.ClientError as e:
        print(f"Netlify HTTP error: {e}")
    except Exception as e:
        print(f"Netlify error: {type(e).__name__}: {e}")
    return None


# ─── VERCEL DEPLOY ────────────────────────────────────────────────────────────
async def deploy_to_vercel(extract_dir: str, token: str, project_name: str) -> str:
    files_to_upload = []
    file_contents = {}

    for root, _, files in os.walk(extract_dir):
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, extract_dir).replace('\\', '/')
            with open(path, 'rb') as f:
                content = f.read()
            sha1 = hashlib.sha1(content).hexdigest()
            files_to_upload.append({
                "file": rel_path,
                "sha": sha1,
                "size": len(content)
            })
            file_contents[sha1] = content

    headers = {"Authorization": f"Bearer {token}"}

    try:
        connector = aiohttp.TCPConnector(ssl=_SSL_CTX)
        async with aiohttp.ClientSession(connector=connector) as session:
            for sha1, content in file_contents.items():
                async with session.post(
                    "https://api.vercel.com/v2/files",
                    headers={**headers, "x-vercel-digest": sha1, "Content-Length": str(len(content))},
                    data=content
                ) as upload_resp:
                    if upload_resp.status not in [200, 201]:
                        err = await upload_resp.text()
                        print(f"Vercel upload error ({sha1[:8]}): {err[:200]}")

            proj_name = project_name.lower().replace('_', '-').replace(' ', '-')[:50]
            payload = {
                "name": proj_name,
                "files": files_to_upload,
                "projectSettings": {"framework": None}
            }
            async with session.post(
                "https://api.vercel.com/v13/deployments",
                headers=headers,
                json=payload
            ) as resp:
                body = await resp.text()
                if resp.status in [200, 201]:
                    data = json.loads(body)
                    url = "https://" + data.get("url", "")
                    print(f"Vercel deployed: {url}")
                    return url
                else:
                    print(f"Vercel deploy error ({resp.status}): {body[:200]}")

    except Exception as e:
        print(f"Vercel deploy exception: {e}")

    return None
