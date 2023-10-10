class XgressScraper:

    def __init__(self) -> None:
        self.host: str = "https://xgress.com/api/v3"

    def to_tuple(self, portals: list[dict]) -> list[tuple]:
        portals_tuples = [self._process_portal(portal) for portal in portals]

        return portals_tuples

    @staticmethod
    def _process_portal(portal: dict) -> tuple:
        portal_tuple: tuple = ()

        for key, value in portal.items():
            if key in ['late6', 'lnge6']:
                portal_tuple = portal_tuple + (value / 1e6,)
            elif key != 'location':
                portal_tuple = portal_tuple + (value,)

        return portal_tuple
