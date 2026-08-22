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

    def load(self):
        if not self.idx_path.exists() or not self.docmap_path.exists():
            raise FileNotFoundError("Index files not found in cache")
        with open(self.idx_path, "rb") as f:
            self.idx = pickle.load(f)
        with open(self.docmap_path, "rb") as f:
            self.docmap = pickle.load(f)


def build():  # builds inverted idx and saves it to disk
    idx = InvertedIndex()
    idx.build()
    idx.save()
    print("Built index and saved to cache")


def remove_stopwords(toks: list[str]) -> list[str]:
    stopwords = load_stopwords()
    return [tok for tok in toks if tok not in stopwords]


def normalize(txt: str) -> list[str]:
    txt = txt.lower()
    no_punct = txt.translate(str.maketrans("", "", string.punctuation))
    toks = remove_stopwords(no_punct.split())
    return [stemmer.stem(tok) for tok in toks]


def search(query: str, n_res: int) -> list:
    idx = InvertedIndex()
    try:
        idx.load()
    except FileNotFoundError:
        print("Error: Index not found. Run 'build' command first.")
        exit(1)

    query_toks = normalize(query)
    if not query_toks:
        return []

    return [] # TODO: put inverted index search logic here
