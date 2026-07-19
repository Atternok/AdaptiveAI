import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE = os.path.join(BASE_DIR, "data", "cache.json")


def load_cache():
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "w") as f:
            json.dump({}, f)

    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)


def check_cache(question):
    cache = load_cache()

    key = question.lower().strip()

    if key in cache:
        return True, cache[key]

    return False, None


def add_cache(question, answer):
    cache = load_cache()

    cache[question.lower().strip()] = answer

    save_cache(cache)