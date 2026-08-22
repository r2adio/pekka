import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MOVIES_PATH = PROJECT_ROOT / "data" / "movies.json"
STOPWORDS_PATH = PROJECT_ROOT / "data" / "stop_words.txt"
CACHE_PATH = PROJECT_ROOT / "cache"


_movies: list[dict] | None = None


def load_movies() -> list[dict]:
    global _movies
    if _movies is None:
        with MOVIES_PATH.open("r", encoding="utf-8") as f:
            _movies = json.load(f)["movies"]
    assert _movies is not None
    return _movies


_stopwords: set[str] | None = None


def load_stopwords() -> set[str]:
    global _stopwords
    if _stopwords is None:
        with STOPWORDS_PATH.open("r", encoding="utf-8") as f:
            _stopwords = set(f.read().splitlines())
    return _stopwords
