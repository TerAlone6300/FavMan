import json
import os
from pathlib import Path

FAV_DIR = Path.home() / ".fav"
DIR_FILE = FAV_DIR / "dirman.json"
FILE_FILE = FAV_DIR / "fileman.json"

def ensure_storage():
    FAV_DIR.mkdir(parents=True, exist_ok=True)
    for f in [DIR_FILE, FILE_FILE]:
        if not f.exists():
            with open(f, "w") as f_out:
                json.dump({}, f_out)

def _load(path):
    ensure_storage()
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def _save(path, data):
    ensure_storage()
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_dirs():
    return _load(DIR_FILE)

def save_dirs(data):
    _save(DIR_FILE, data)

def load_files():
    return _load(FILE_FILE)

def save_files(data):
    _save(FILE_FILE, data)

def add_entry(is_file, alias, path):
    data = load_files() if is_file else load_dirs()
    data[alias] = str(Path(path).resolve())
    if is_file:
        save_files(data)
    else:
        save_dirs(data)

def remove_entry(is_file, alias):
    data = load_files() if is_file else load_dirs()
    if alias in data:
        del data[alias]
        if is_file:
            save_files(data)
        else:
            save_dirs(data)
        return True
    return False

def get_path(is_file, alias):
    data = load_files() if is_file else load_dirs()
    return data.get(alias)
