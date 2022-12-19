from src.models.generic import Generic
from src.api import get_location_data
from src.models.market import Market

class Location(Generic):
    def __init__(self, location_id = None, data = None, store = None):
        super().__init__(first_id = location_id, data = data, data_function = get_location_data, store = store)

    def locator(self):
        return self.symbol

    def get_ships(self):
        return [ship for ship in self.store.ships if ship.location == self]

    def get_system(self):
        return self.symbol.split('-')[0]

    def has_market(self):
        return self.symbol in [market.location_id for market in self.store.markets]

    def get_market(self):
        if self.has_market():
            return [market for market in self.store.markets if market.location_id == self.symbol][0]
        else:
            return Market(location_id = self.symbol, store = self.store)