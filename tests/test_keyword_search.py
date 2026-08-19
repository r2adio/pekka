"""NOTE:
assert results == [ "A", "B", "C" ] # exact contents and order
assert set(results) == { "A", "B", "C" } # exact contents and commutative
assert "A" in results; assert "B" in results # atleast these items and commutative"""

import pytest

from cli.lib.search import search

MOVIE_DATA = [
    {"id": 0, "title": "The Great Valley Adventure"},
    {"id": 1, "title": "The First Great Train Robbery"},
    {"id": 2, "title": "No Country for Old Men"},
    {"id": 3, "title": "The Wonderful Country"},
    {"id": 4, "title": "The Country Bears"},
    {"id": 5, "title": "It's Magic, Charlie Brown"},
    {"id": 6, "title": "Furious Seven"},
    {"id": 7, "title": "Fast and Furious"},
    {"id": 8, "title": "Faster, Pussycat! Kill! Kill!"},
    {"id": 9, "title": "Hot Potato"},
    {"id": 10, "title": "Hotel Chevalier"},
    {"id": 11, "title": "Killshot"},
]


@pytest.fixture
def movies(monkeypatch):
    monkeypatch.setattr("cli.lib.search.load_movies", lambda: MOVIE_DATA)


def test_keyword_search(movies):
    assert search("Great", 5) == [
        "The Great Valley Adventure",
        "The First Great Train Robbery",
    ]


def test_preprocessing(movies):
    results = search("country", 5)
    assert "No Country for Old Men" in results
    assert "The Wonderful Country" in results
    assert "The Country Bears" in results


def test_punctuation(movies):
    assert search("magic charlie", 5) == ["It's Magic, Charlie Brown"]


def test_tokenization(movies):
    assert search("furious fast", 5) == [
        "Furious Seven",
        "Fast and Furious",
        "Faster, Pussycat! Kill! Kill!",
    ]


def test_stopwords(movies):
    assert search("the hot shot", 5) == [
        "Hot Potato",
        "Hotel Chevalier",
        "Killshot",
    ]
