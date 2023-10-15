import argparse
import time

from xgress_scraper import XgressScraper


def single_query(query: str) -> None:
    print('Searching for portals...\n')
    return xgress.search_portals(query)


def list_queries(filepath: str) -> None:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                print(line.strip())
                xgress.search_portals(line.strip())
                time.sleep(18)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main(data: str, queries_list: bool = False) -> None:
    if queries_list:
        return list_queries(data)

    return single_query(data)


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', type=str, help='Search query')
    parser.add_argument('-l', '--list', type=str, help="Path to a file with a list of queries")

    args: argparse.Namespace = parser.parse_args()
    xgress: XgressScraper = XgressScraper()

    if args.query:
        main(args.query)
    if args.list:
        main(args.list, True)
