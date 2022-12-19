from src.models.generic import Generic
import datetime
from src.api import get_market_data


class Market(Generic):
    def __init__(self, location_id = None, data = None, store = None):
        super().__init__(first_id = location_id, data = data, data_function=get_market_data, store = store)
        if location_id is not None: # If loading from api, need to add location and date
            self.location_id = location_id
            self.date = str(datetime.datetime.now())

    def locator(self):
        return self.location_id

    def update_from_api(self): # markets are not updated, so this is a no-op. Create a new market instead
        raise Exception('Markets are not updated')
