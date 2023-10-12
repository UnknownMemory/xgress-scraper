import time
from requests import post, RequestException, Response

from xgress_scraper import Database


class XgressScraper:

    def __init__(self) -> None:
        self.host: str = 'https://xgress.com/api/v3'
        self.headers: dict = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0',
                              'Content-Type': 'application/json;charset=UTF-8',
                              'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
                              'Sec-Ch-Ua-Mobile': '?0',
                              'Sec-Ch-Ua-Platform': 'Windows',
                              'Origin': 'https://xgress.com',
                              'Sec-Fetch-Site': 'same-origin',
                              'Sec-Fetch-Mode': 'cors',
                              'Sec-Fetch-Dest': 'empty',
                              'Referer': 'https://xgress.com/portal_search'
                             }
        self.database: Database = Database()

    def search_portals(self, query: str) -> None:
        total: int = 0
        offset: int = 0

        while True:
            if total > 0 and offset > 0 and total == offset:
                break
            try:
                response: Response = post(self.host, json={'request': 'portals_search', 'args': {'portal': query, 'limit': 10000, 'offset': offset}}, headers=self.headers)
                search_result: dict = response.json()['result']

                if search_result['count'] == 0:
                    break

                self.save_portals(search_result['portals_search'])
                total = search_result['total']
                offset += search_result['count']

                time.sleep(15)

            except RequestException as e:
                print(e)
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
        keys = ['name', 'pguid', 'short', 'img', 'address', 'description', 'late6', 'lnge6']
        previous_key: str = ''
        portal_tuple: tuple = ()

        for key, value in portal.items():
            if previous_key and key not in ['location', 'status'] and key != keys[keys.index(previous_key) + 1]:
                portal_tuple += ('',)
            if key in ['late6', 'lnge6']:
                portal_tuple += (value / 1e6,)
            elif key not in ['location', 'status']:
                portal_tuple += (value,)

            previous_key = key if key in keys else ''
        return portal_tuple
