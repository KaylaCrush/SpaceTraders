from src.api import *
from src.store import *
import datetime

class Generic:
    def __init__(self, first_id = None, second_id = None, data=None, data_function = None):
        if data is not None:
            self.__dict__.update(data)
        elif data_function is not None:
            if first_id is not None and second_id is not None:
                self.__dict__.update(data_function(first_id, second_id))
            elif first_id is not None:
                self.__dict__.update(data_function(first_id))
        else:
            raise Exception('No id or data given')

class Ship(Generic):
    def __init__(self, ship_id=None, data = None):
        super().__init__(first_id = ship_id, data=data, data_function=get_ship_data)

    def has_location(self):
        return self.location is not None

    def travel_to(self, destination):
        if self.has_location():
            pass

    def make_flightplan(self, destination):
        if self.has_location():
            return FlightPlan(self.id, destination)


class Location(Generic):
    def __init__(self, location_id=None, data = None):
        super().__init__(first_id = location_id, data=data, data_function=get_location_data)


class System(Generic):
    def __init__(self, system_id=None, data = None):
        super().__init__(first_id = system_id, data=data, data_function=get_system_data)


class Structure(Generic):
    def __init__(self, structure_id=None, data = None):
        super().__init__(first_id = structure_id, data = data, data_function=get_structure_data)


class Market(Generic):
    def __init__(self, location_id = None, data = None):
        super().__init__(first_id = location_id, data = data, data_function=get_market_data)
        self.location_id = location_id
        self.date = str(datetime.datetime.now())


class FlightPlan(Generic):
    def __init__(self, ship_id = None, destination = None, data = None):
        super().__init__(first_id = ship_id, second_id = destination, data = data, data_function=make_flightplan)