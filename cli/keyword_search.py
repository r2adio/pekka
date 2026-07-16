import argparse
import json


def load_data():
    with open("./data/movies.json", "r") as f:
        data = json.load(f)
        return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            # output all the titles:
            # titles = [movie["title"] for movie in load_data()["movies"]]
            # print(titles)
            search_query = args.query.lower()
            matching_titles = [
                movie["title"]
                for movie in load_data()["movies"]
                if search_query in movie["title"].lower()
            ]
            print(matching_titles)

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
