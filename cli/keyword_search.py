import argparse
import json

def load_data():
    with open("./data/movies.json", "r") as f:
        data = json.load(f)
        return data


def get_results(search_query: str) -> list:
    matching_titles: list = [
        movie["title"]
        for movie in load_data()["movies"]
        if search_query in movie["title"].lower()
    ][:5]
    return matching_titles


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            search_query: str = args.query.lower()
            # get_results(search_query)
            print(f"SEARCHING FOR: {search_query}")
            for i, movie_name in enumerate(get_results(search_query)):
                print(f"{i + 1}. {movie_name}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
