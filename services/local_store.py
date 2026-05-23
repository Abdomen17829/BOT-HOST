import json
import os
import threading

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.json")

_lock = threading.Lock()

def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def _read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_json(path, data):
    _ensure_dir()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    os.replace(tmp, path)

def get_user(user_id):
    with _lock:
        users = _read_json(USERS_FILE)
        return users.get(str(user_id))

def upsert_user(user_id, updates):
    with _lock:
        users = _read_json(USERS_FILE)
        key = str(user_id)
        if key in users:
            users[key].update(updates)
        else:
            users[key] = {"user_id": user_id, **updates}
        _write_json(USERS_FILE, users)

def get_projects(user_id):
    with _lock:
        projects = _read_json(PROJECTS_FILE)
        return projects.get(str(user_id), [])

def add_project(user_id, project_name, live_url, seo_score):
    with _lock:
        projects = _read_json(PROJECTS_FILE)
        key = str(user_id)
        if key not in projects:
            projects[key] = []
        projects[key].append({
            "project_name": project_name,
            "live_url": live_url,
            "seo_score": seo_score,
            "created_at": __import__("datetime").datetime.utcnow().isoformat()
        })
        _write_json(PROJECTS_FILE, projects)
