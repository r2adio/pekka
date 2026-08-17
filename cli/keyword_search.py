import argparse

from lib.search import search


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
            for i, movie_name in enumerate(search(search_query)):
                print(f"{i + 1}. {movie_name}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
