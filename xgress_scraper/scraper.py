from xgress_scraper import Database


class XgressScraper:

    def __init__(self) -> None:
        self.host: str = "https://xgress.com/api/v3"
        self.database = Database()

    def add_portals(self, portals: list[dict]) -> None:
        portals_tuples = [self._process_portal(portal) for portal in portals]

        self.database.begin_transaction(portals_tuples)
        self.database.end_transaction()

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
