import os
import pickle
import string
from collections import defaultdict

from nltk.stem import PorterStemmer

from .search_utils import CACHE_PATH, load_movies, load_stopwords

stemmer = PorterStemmer()


class InvertedIndex:
    def __init__(self) -> None:
        self.idx = defaultdict(set)  # dict of sets, token: [doc_id1, doc_id2, ..]
        self.docmap = {}  # map document ID : document
        self.idx_path = CACHE_PATH / "index.pkl"
        self.docmap_path = CACHE_PATH / "docmap.pkl"

    def __add_document(self, doc_id, txt):
        # normalize txt into tokens and add each token and its doc_id to idx
        tokens = normalize(txt)
        for token in tokens:
            self.idx[token].add(doc_id)

    def get_documents(self, term):
        # sorted list of doc_id for every preprocessed token
        return sorted(self.idx[term])  # sorted() always returns a new list

    def build(self):
        for m in load_movies():
            doc_id = m["id"]
            text = f"{m['title']} {m['description']}"
            self.__add_document(doc_id, text)
            self.docmap[doc_id] = m

    def save(self):
        os.makedirs(CACHE_PATH, exist_ok=True)
        with open(self.idx_path, "wb") as f:
            pickle.dump(self.idx, f)
        with open(self.docmap_path, "wb") as f:
            pickle.dump(self.docmap, f)


def build():  # builds inverted idx and saves it to disk
    idx = InvertedIndex()
    idx.build()
    idx.save()
    docs = idx.get_documents("merida")  # get doc for token
    print(f"First document for token 'merida' = {docs[0]}")


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
    for m in load_movies():
        if len(matching_titles) >= n_res:
            break
        title_toks = normalize(m["title"])
        # match query fragments (sub-string) within title tokens, eg: "hot" -> "hotel"
        if any(
            query_tok in title_tok
            for query_tok in query_toks
            for title_tok in title_toks
        ):
            matching_titles.append(m["title"])

    return matching_titles
