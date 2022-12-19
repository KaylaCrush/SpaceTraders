
from src.models.generic import Generic
from src.models.flightplan import FlightPlan
from src.models.transaction import Transaction
from math import hypot
from src.api import get_ship_data

class Ship(Generic):
    def __init__(self, ship_id:str = None, data:dict = None, store = None):
        super().__init__(first_id = ship_id, data = data, data_function = get_ship_data, store = store)

    @property
    def name(self):
        return f"{self.manufacturer} {'-'.join(self.type.split('-')[1:])}"

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
        return hypot(self.x-location.x, self.y-location.y)
    
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

# ship = Ship()
# ship.move(Navigator.find_next_location(ship))

# # alternative

# Navigator.move(ship)

# class Navigator:
#     def move(ship):
#         # v1
#         PriceAnalyzer.get_most_profitable_location(ship)

#         # ML version
#         optimal_location = self.ml_model.generate_profit_map().get_best_location(ship)
#         return optimal_location

# Ship => Navigator

# ship.move(Navigator.find_next_location(ship))

# Ship <=> Navigator