import json
from src.models import *
from os.path import exists

KNOWN_SYSTEMS = ["OE"]

class Store:
    def __init__(self, load_from_file = True):
        self.systems = []
        self.ships = []
        self.locations = []
        self.markets = []
        self.structures = []

        self.flightplans = []
        self.loans = []
        self.transactions = []
        self.types = {}
        self.user = None

        if load_from_file and exists('data/systems.json'):
            self.update_from_file()
        else:
            self.update_from_api()
        self.save_to_file()

    def get_ship(self, id):
        return [ship for ship in self.ships if ship.id == id][0]

    def get_location(self, id):
        return [location for location in self.locations if location.symbol == id][0]
    
    def get_market(self, location_id):
        if location_id in [market.location_id for market in self.markets]:
            return [market for market in self.markets if market.location_id == location_id][0]
        else:
            return Market(location_id = location_id, store = self)

    def update_from_file(self):
        for key in self.__dict__.keys():
            if exists('data/' + key + '.json'):
                with open('data/' + key + '.json', 'r') as f:
                    if key == 'user':
                        self.user = User(store = self, data = json.load(f))
                    elif key == 'types':
                        self.types = json.load(f)
                    else:
                        self.__dict__[key] = [globals()[key.capitalize()[:-1]](data = data, store = self) for data in json.load(f)]
                    

    def save_to_file(self):
        for key in self.__dict__.keys():
            if exists('data/' + key + '.json'):
                with open('data/' + key + '.json', 'w') as f:
                    if key == 'user':
                        json.dump(self.user.my_data(), f, indent=4)
                    elif key == 'types':
                        json.dump(self.types, f, indent=4)
                    else:
                        json.dump([value.my_data() for value in self.__dict__[key]], f, indent=4)


    def update_from_api(self):
        self.user = User(store = self)
        for system_id in KNOWN_SYSTEMS:
            System(system_id, store = self)
        for ship in get_ships():
            Ship(ship_id = ship['id'], store = self)
        for system_id in KNOWN_SYSTEMS:
            for location in get_system_locations(system_id):
                Location(location_id = location['symbol'], store = self)
        for ship in self.ships:
            if ship.has_location():
                Market(location_id = ship.location, store = self)
        for structure in get_my_structures():
            Structure(structure_id = structure['id'], store = self)

        self.types['goods'] = get_available_goods()
        self.types['loans'] = get_available_loans()
        self.types['structures'] = get_available_structures()
        self.types['ships'] = get_available_ships()
        self.types['shipyards'] = []
        for system_id in KNOWN_SYSTEMS:
            self.types['shipyards'].append(get_system_ship_listings(system_id))