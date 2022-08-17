from src.api import *
from src.store import *
import datetime
import math
import threading

################################################################################
# Classes
################################################################################

class Generic:
    def __init__(self, 
    first_id:str = None, 
    second_id:str = None, 
    data:dict = None, 
    store = None,
    data_function = None, 
    update_function = None):

        # data_function is called when opject is initalized with no data
        # update_function is called when object is updated
        self.data_function = data_function if data_function else None
        self.update_function = update_function if update_function else data_function

        # if data is provided, populate self from the data
        if data: self.__dict__.update(data)

        # if no data is provided, call the data_function to get the data, if it exists
        elif self.data_function:
            if first_id:
                if second_id:
                    self.__dict__.update(data_function(first_id, second_id))
                else:
                    self.__dict__.update(data_function(first_id))
        else:
            raise Exception('No data or data_function provided')

        # if store is provided, add self to the store
        if store:
            self.store = store
            self.store.__dict__[self.__class__.__name__.lower() + 's'].append(self) # fancy way to get the class name

    def my_data(self): ## essentially a version of __dict__ that excludes the store and data functions, for saving purposes
        return {key:value for key, value in self.__dict__.items() if key not in ['store', 'data_function', 'update_function']}

    def locator(self): #returns whatever you feed into the data function to complete the api call
        return self.id  # this is the default behavior for most classes

    def update_from_api(self): # updates the object from the api
        self.__dict__.update(self.update_function(self.locator())) 
        return self.__dict__

    def update_from_data(self, data): # updates the object from a dictionary of data
        self.__dict__.update(data)
        return self.__dict__

class Ship(Generic):
    def __init__(self, ship_id:str = None, data:dict = None, store = None):
        super().__init__(first_id = ship_id, data = data, data_function = get_ship_data, store = store)

    def has_location(self):
        return hasattr(self,'location')

    def travel_to(self, destination):
        if self.has_location():
            return FlightPlan(self.id, destination)
        else:
            raise Exception('Ship has no location (likely in flight already)')

    def purchace_good(self, good_id:str, amount:int):
        return self.make_transaction('purchace', good_id, amount)

    def sell_good(self, good_id:str, amount:int):
        return self.make_transaction('sell', good_id, amount)
    
    def make_transaction(self, transaction_type:str, good_id:str, amount:int):
        if transaction_type not in ['purchace', 'sell']:
            raise Exception('Invalid transaction type')
        if transaction_type == 'purchace':
            response = self.purchace_good(good_id, amount)
        elif transaction_type == 'sell':
            response = self.sell_good(good_id, amount)
        self.upddate_from_data(response['ship'])
        Transaction(transaction_type, response)
        return response

    def distance_to(self, location):
        return math.hypot(self.x-location.x, self.y-location.y)
    
    def get_cargo_good(self, good_id:str):
        for cargo in self.cargo:
            if cargo['good'] == good_id:
                return cargo
        return None

    def get_good_quantity(self, good_id:str):
        if self.get_cargo_good(good_id):
            return self.get_cargo_good(good_id)['quantity']
        else:
            return 0

    def get_good_volume(self, good_id:str):
        if self.get_cargo_good(good_id):
            return self.get_cargo_good(good_id)['totalVolume']
        else:
            return 0

    def get_fuel(self):
        return self.get_good_quantity('FUEL')

class Navigator():
    def __init__(self):
        self.ships = []
        self.routes = []

    def add_ship(self, ship:Ship):
        self.ships.append(ship)

    def add_route(self, route):
        self.routes.append(route)


# a route is a list of waypoints
class Route():
    def __init__(self, waypoints:list = None, name = None):
        self.waypoints = waypoints if waypoints else []
        self.name = name if name else 'Unnamed Route'

class Waypoint():
    def __init__(self, location_id:str, buy:list = None, sell:list = None):
        self.location_id = location_id
        self.buy = buy if buy else []
        self.sell = sell if sell else []

class Location(Generic):
    def __init__(self, location_id = None, data = None, store = None):
        super().__init__(first_id = location_id, data = data, data_function = get_location_data, store = store)

    def locator(self):
        return self.symbol

    def get_ships(self):
        return [ship for ship in self.store.ships if ship.location == self]

    def get_system(self):
        return self.symbol.split('-')[0]

class System(Generic):
    def __init__(self, system_id=None, data = None, store = None):
        super().__init__(first_id = system_id, data=data, data_function=get_system_data, store = store)

    def locator(self):
        return self.symbol

    def get_locations(self):
        return [location for location in self.store.locations if location.symbol.startswith(self.symbol)]


class Structure(Generic):
    def __init__(self, structure_id = None, data = None, store = None):
        super().__init__(first_id = structure_id, data = data, data_function=get_structure_data, store = store)

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


class FlightPlan(Generic):
    def __init__(self, ship_id = None, destination = None, data = None, store = None):
        super().__init__(first_id = ship_id, second_id = destination, data = data, data_function = make_flightplan, update_function = get_flightplan, store = store)

class Loan(Generic):
    def __init__(self, data, store = None):
        super().__init__(data = data, store = store)

class Transaction(Generic):
    def __init__(self, transaction_type:str, data, store = None):
        data['transaction_type'] = transaction_type
        super().__init__(data = data, store = store)

class User(Generic):
    def __init__(self, data = None, username = USERNAME, store = None):
        super().__init__(first_id = username, data = data, data_function = get_my_status, store = store)