import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MOVIES_PATH = PROJECT_ROOT / "data" / "movies.json"
STOPWORDS_PATH = PROJECT_ROOT / "data" / "stop_words.txt"


def load_movies() -> list[dict]:
    with MOVIES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)["movies"]


def load_stopwords():
    with STOPWORDS_PATH.open("r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}
