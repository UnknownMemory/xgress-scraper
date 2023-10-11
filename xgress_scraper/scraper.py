import time
from requests import post, RequestException, Response

from xgress_scraper import Database


class XgressScraper:

    def __init__(self) -> None:
        self.host: str = "https://xgress.com/api/v3"
        self.database: Database = Database()

    def search_portals(self, query: str) -> None:
        offset: int = 0

        while True:
            try:
                response: Response = post(self.host, {'requests': 'portal_search', 'args': {'portal': query, 'limit': 10000, 'offset': offset}})
                search_result: dict = response.json()['result']

                if search_result['total'] == 0:
                    break

                self.save_portals(search_result['portals_search'])
                offset += search_result['count']

                time.sleep(15)

            except RequestException:
                break

        if self.database.transactions > 0:
            save_transactions = self.database.end_transaction()
            print(save_transactions)

        print('No result found for this query')

    def save_portals(self, portals: list[dict]) -> None:
        portals_tuples = [self._process_portal(portal) for portal in portals]
        begin_transaction = self.database.begin_transaction(portals_tuples)

        print(begin_transaction)

    @staticmethod
    def _process_portal(portal: dict) -> tuple:
        previous_key: str = ''
        portal_tuple: tuple = ()

        for key, value in portal.items():
            if previous_key == 'address' and key != 'description':
                portal_tuple += ('',)
            if key in ['late6', 'lnge6']:
                portal_tuple += (value / 1e6,)
            elif key not in ['location', 'status']:
                portal_tuple += (value,)

            previous_key = key

        return portal_tuple
