from src.models.generic import Generic
from src.api import get_system_data


class System(Generic):
    def __init__(self, system_id=None, data = None, store = None):
        super().__init__(first_id = system_id, data=data, data_function=get_system_data, store = store)

    def locator(self):
        return self.symbol

    def get_locations(self):
        return [location for location in self.store.locations if location.symbol.startswith(self.symbol)]