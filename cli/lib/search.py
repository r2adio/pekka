import string

from nltk.stem import PorterStemmer

from .search_utils import load_movies, load_stopwords

stemmer = PorterStemmer()


def remove_stopwords(toks: list[str]) -> list[str]:
    return [tok for tok in toks if tok not in load_stopwords()]


def normalize(txt: str) -> list[str]:
    txt = txt.lower()
    no_punct = txt.translate(str.maketrans("", "", string.punctuation))
    toks = remove_stopwords(no_punct.split())
    return [stemmer.stem(tok) for tok in toks]


def search(query: str, n_res: int) -> list:
    query_toks = normalize(query)
    if not query_toks:
        return []

    matching_titles: list = []
    for movie in load_movies():
        if len(matching_titles) >= n_res:
            break
        title_toks = normalize(movie["title"])
        # match query fragments (sub-string) within title tokens, eg: "hot" -> "hotel"
        if any(
            query_tok in title_tok
            for query_tok in query_toks
            for title_tok in title_toks
        ):
            matching_titles.append(movie["title"])

    return matching_titles
