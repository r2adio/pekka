import argparse
import json
import string
from pathlib import Path

STOP_WORDS_PATH = Path(__file__).parent.parent / "data" / "stop_words.txt"
STOP_WORDS = {
    word.strip()
    # for word in Path("data/stop_words.txt").read_text().splitlines()  # relative to cwd
    for word in STOP_WORDS_PATH.read_text(
        encoding="utf-8"
    ).splitlines()  # relative to file
    if word.strip()
}


def load_data():
    with open("./data/movies.json", "r") as f:
        data = json.load(f)
        return data


def tokenize(text: str) -> list[str]:
    return text.split()


def remove_stop_words(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token not in STOP_WORDS]


def normalize(text: str) -> list[str]:
    lowered = text.lower()
    no_punct = lowered.translate(str.maketrans("", "", string.punctuation))
    tokens = tokenize(no_punct)
    return remove_stop_words(tokens)


def get_results(search_query: str) -> list:
    query_tokens = normalize(search_query)
    if not query_tokens:
        return []

    matching_titles: list = []
    for movie in load_data()["movies"]:
        title_tokens = normalize(movie["title"])
        if all(token in title_tokens for token in query_tokens):
            matching_titles.append(movie["title"])

    return matching_titles[:5]


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            search_query: str = args.query
            # get_results(search_query)
            print(f"SEARCHING FOR: {search_query}")
            for i, movie_name in enumerate(get_results(search_query)):
                print(f"{i + 1}. {movie_name}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
