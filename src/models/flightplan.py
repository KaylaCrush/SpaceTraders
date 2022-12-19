from src.models.generic import Generic
from src.api import *

class FlightPlan(Generic):
    def __init__(self, ship_id = None, destination = None, data = None, store = None):
        super().__init__(first_id = ship_id, second_id = destination, data = data, data_function = make_flightplan, update_function = get_flightplan, store = store)