import string

from lib.search_utils import load_data, load_stopwords


def tokenize(text: str) -> list[str]:
    return text.split()


def remove_stopwords(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token not in load_stopwords()]


def normalize(text: str) -> list[str]:
    lowered = text.lower()
    no_punct = lowered.translate(str.maketrans("", "", string.punctuation))
    tokens = tokenize(no_punct)
    return remove_stopwords(tokens)


def search(search_query: str) -> list:
    query_tokens = normalize(search_query)
    if not query_tokens:
        return []

    matching_titles: list = []
    for movie in load_data():
        title_tokens = normalize(movie["title"])
        if all(token in title_tokens for token in query_tokens):
            matching_titles.append(movie["title"])

    return matching_titles[:5]
