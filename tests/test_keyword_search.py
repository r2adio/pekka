import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cli.keyword_search import get_results, normalize, tokenize, remove_stop_words

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


def test_tokenize():
    assert tokenize("the matrix") == ["the", "matrix"]
    assert tokenize("hello world") == ["hello", "world"]
    assert tokenize("single") == ["single"]
    assert tokenize("") == []


def test_remove_stop_words():
    assert remove_stop_words(["the", "matrix"]) == ["matrix"]
    assert remove_stop_words(["a", "puppy"]) == ["puppy"]
    assert remove_stop_words(["hello", "world"]) == ["hello", "world"]
    assert remove_stop_words(["the", "a", "an"]) == []


def test_normalize():
    assert normalize("The Matrix") == ["matrix"]
    assert normalize("HE IS HERE") == ["here"]
    assert normalize("Hello, World!") == ["hello", "world"]
    assert normalize("sci-fi") == ["scifi"]
    assert normalize("the a an") == []


@patch("cli.keyword_search.load_data", return_value=MOVIE_DATA)
def test_returns_multiple_matches(mock):
    assert get_results("zzz") == []
    assert get_results("alpha") == ["alpha"]
    assert mock.call_count == 2


@patch("cli.keyword_search.load_data", return_value=MOVIE_DATA)
def test_search_with_case_and_punctuation(_mock):
    assert get_results("MATRIX") == ["The Matrix"]
    assert get_results("hello world") == ["Hello, World!"]
    assert get_results("sci-fi") == ["sci-fi Heroes"]


@patch("cli.keyword_search.load_data", return_value=MOVIE_DATA)
def test_search_with_stop_words(_mock):
    assert get_results("the matrix") == ["The Matrix"]
    assert get_results("a puppy") == []
    assert get_results("matrix heroes") == []
    assert get_results("sci-fi heroes") == ["sci-fi Heroes"]
