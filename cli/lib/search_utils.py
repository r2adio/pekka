import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MOVIES_PATH = PROJECT_ROOT / "data" / "movies.json"
STOPWORDS_PATH = PROJECT_ROOT / "data" / "stop_words.txt"
CACHE_PATH = PROJECT_ROOT / "cache"


def load_movies() -> list[dict]:
    with MOVIES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)["movies"]


def load_stopwords():
    with STOPWORDS_PATH.open("r", encoding="utf-8") as f:
        return f.read().splitlines()  # .readlines() keeps \n or \r\n attached
