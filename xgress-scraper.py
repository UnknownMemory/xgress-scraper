import argparse

from xgress_scraper import XgressScraper


def main(query: str) -> None:
    xgress: XgressScraper = XgressScraper()

    print('Searching for portals...\n')
    xgress.search_portals(query)


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('query', help='Search query')

    args: argparse.Namespace = parser.parse_args()

    main(args.query)
