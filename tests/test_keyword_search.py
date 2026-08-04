import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cli.keyword_search import get_results

MOVIE_DATA = {
    "movies": [
        {"id": 1, "title": "The Matrix"},
        {"id": 2, "title": "sci-fi Heroes"},
        {"id": 3, "title": "Hello, World!"},
        {"id": 4, "title": "HE IS HERE"},
        {"id": 5, "title": "alpha"},
        {"id": 6, "title": "beta"},
        {"id": 7, "title": "gamma"},
        {"id": 8, "title": "delta"},
    ]
}


@patch("cli.keyword_search.load_data", return_value=MOVIE_DATA)
def test_returns_multiple_matches(mock):
    assert len(get_results("a")) == 5
    assert get_results("zzz") == []
    assert mock.call_count == 2


@patch("cli.keyword_search.load_data", return_value=MOVIE_DATA)
def test_search_with_case_and_punctuation(_mock):
    assert get_results("MATRIX") == ["The Matrix"]
    assert get_results("hello world") == ["Hello, World!"]
    assert get_results("sci-fi") == ["sci-fi Heroes"]
