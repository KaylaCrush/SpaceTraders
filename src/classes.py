from src.api import *
from src.store import *
import datetime

class Generic:
    data_function = None #this is the function that gets the data from the api

    def __init__(self, first_id:str = None, second_id:str = None, data:dict=None, data_function = None):
        if data is not None:
            self.__dict__.update(data)
        elif data_function is not None:
            if first_id is not None:
                if second_id is not None:
                    self.__dict__.update(data_function(first_id, second_id))
                else:
                    self.__dict__.update(data_function(first_id))
        else:
            raise Exception('No id or data given')
    
    def my_data(self): ## essentially a version of __dict__ that excludes the store, for saving purposes
        return {key:value for key, value in self.__dict__.items() if key not in 'store'}

    def locator(self): #returns whatever you feed into the data function to complete the api call
        return self.id #this is the default behavior for most classes

    def update_from_api(self): #updates the object from the api
        self.__dict__.update(self.data_function(self.locator())) 


class Ship(Generic):
    data_function = get_ship_data
    def __init__(self, ship_id:str = None, data:dict = None, store = None):
        super().__init__(first_id = ship_id, data = data, data_function = Ship.data_function)
        if store is not None:
            self.store = store
            store.ships.append(self)

    def has_location(self):
        return self.location is not None

    def travel_to(self, destination):
        flightplan = make_flightplan(destination)

    def make_flightplan(self, destination):
        if self.has_location():
            return FlightPlan(self.id, destination)


class Location(Generic):
    data_function = get_location_data
    def __init__(self, location_id=None, data = None, store = None):
        super().__init__(first_id = location_id, data=data, data_function=Location.data_function)
        if store is not None:
            self.store = store
            store.locations.append(self)

    def locator(self):
        return self.symbol


class System(Generic):
    data_function = get_system_data
    def __init__(self, system_id=None, data = None, store = None):
        super().__init__(first_id = system_id, data=data, data_function=System.data_function)
        if store is not None:
            self.store = store
            store.systems.append(self)

    def locator(self):
        return self.symbol


class Structure(Generic):
    data_function = get_structure_data
    def __init__(self, structure_id = None, data = None, store = None):
        super().__init__(first_id = structure_id, data = data, data_function=Structure.data_function)
        if store is not None:
            self.store = store
            store.structures.append(self)


class Market(Generic):
    data_function = get_market_data
    def __init__(self, location_id = None, data = None, store = None):
        super().__init__(first_id = location_id, data = data, data_function=Market.data_function)
        if location_id is not None: # If loading from api, need to add location and date
            self.location_id = location_id
            self.date = str(datetime.datetime.now())
        if store is not None:
            self.store = store
            store.markets.append(self)

    def locator(self):
        return self.location_id

    def update_from_api(self): # markets are not updated, so this is a no-op. Create a new market instead
        raise Exception('Markets are not updated')


class FlightPlan(Generic):
    data_function = get_flightplan
    def __init__(self, ship_id = None, destination = None, data = None, store = None):
        super().__init__(first_id = ship_id, second_id = destination, data = data, data_function=make_flightplan)
        if store is not None:
            self.store = store
            store.flightplans.append(self)