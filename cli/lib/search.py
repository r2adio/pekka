import string

from .search_utils import load_movies, load_stopwords


def tokenize(text: str) -> list[str]:
    return text.split()


def remove_stopwords(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token not in load_stopwords()]


def normalize(text: str) -> list[str]:
    lowered = text.lower()
    no_punct = lowered.translate(str.maketrans("", "", string.punctuation))
    tokens = tokenize(no_punct)
    return remove_stopwords(tokens)


def search(query: str, n_res: int) -> list:
    query_tok = normalize(query)
    if not query_tok:
        return []

    matching_titles: list = []
    for movie in load_movies():
        if len(matching_titles) >= n_res:
            break
        title_tokens = normalize(movie["title"])
        if all(token in title_tokens for token in query_tok):
            matching_titles.append(movie["title"])

    return matching_titles
