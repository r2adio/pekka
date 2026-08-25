"""NOTE:
assert results == [ "A", "B", "C" ] # exact contents and order
assert set(results) == { "A", "B", "C" } # exact contents and commutative
assert "A" in results; assert "B" in results # atleast these items and commutative"""

import pytest

from cli.lib.search import InvertedIndex, search

MOVIE_DATA = [
    {"id": 0, "title": "The Great Valley Adventure", "description": "Test movie description."},
    {"id": 1, "title": "The First Great Train Robbery", "description": "Test movie description."},
    {"id": 2, "title": "No Country for Old Men", "description": "Test movie description."},
    {"id": 3, "title": "The Wonderful Country", "description": "Test movie description."},
    {"id": 4, "title": "The Country Bears", "description": "Test movie description."},
    {"id": 5, "title": "It's Magic, Charlie Brown", "description": "Test movie description."},
    {"id": 6, "title": "Furious Seven", "description": "Test movie description."},
    {"id": 7, "title": "Fast and Furious", "description": "Test movie description."},
    {"id": 8, "title": "Faster, Pussycat! Kill! Kill!", "description": "Test movie description."},
    {"id": 9, "title": "Hot Potato", "description": "Test movie description."},
    {"id": 10, "title": "Hotel Chevalier", "description": "Test movie description."},
    {"id": 11, "title": "Killshot", "description": "Test movie description."},
    {"id": 12, "title": "Virginia's Run", "description": "Test movie description."},
    {"id": 13, "title": "Take the Money and Run", "description": "Test movie description."},
    {"id": 14, "title": "Woman on the Run", "description": "Test movie description."},
]


@pytest.fixture
def movies(tmp_path, monkeypatch):
    monkeypatch.setattr("cli.lib.search.CACHE_PATH", tmp_path)
    monkeypatch.setattr("cli.lib.search.load_movies", lambda: MOVIE_DATA)
    idx = InvertedIndex()
    idx.build()
    idx.save()


def test_keyword_search(movies):
    assert search("Great", 5) == [
        ("The Great Valley Adventure", 0),
        ("The First Great Train Robbery", 1),
    ]


def test_preprocessing(movies):
    results = search("country", 5)
    assert ("No Country for Old Men", 2) in results
    assert ("The Wonderful Country", 3) in results
    assert ("The Country Bears", 4) in results


def test_punctuation(movies):
    assert search("magic charlie", 5) == [
        ("It's Magic, Charlie Brown", 5),
        ("It's Magic, Charlie Brown", 5),
    ]


def test_tokenization(movies):
    assert search("furious fast", 5) == [
        ("Furious Seven", 6),
        ("Fast and Furious", 7),
        ("Fast and Furious", 7),
    ]


def test_stopwords(movies):
    assert search("the hot shot", 5) == [("Hot Potato", 9)]


def test_stemming(movies):
    assert search("running", 5) == [
        ("Virginia's Run", 12),
        ("Take the Money and Run", 13),
        ("Woman on the Run", 14),
    ]