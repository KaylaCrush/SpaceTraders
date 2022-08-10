import json
from src.api import *
from src.classes import *
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
        self.types = []
        self.user = {}

        if load_from_file and exists('data/systems.json'):
            self.fill_from_file()
        else:
            self.fill_from_api()

        self.save_to_file()

    def fill_from_file(self):
        for key in self.__dict__.keys():
            if exists('data/' + key + '.json'):
                with open('data/' + key + '.json', 'r') as f:
                    self.__dict__[key] = [globals()[key.capitalize()[:-1]](data = data, store = self) for data in json.load(f)]
                    


    def save_to_file(self):
        for key in self.__dict__.keys():
            if exists('data/' + key + '.json'):
                with open('data/' + key + '.json', 'w') as f:
                    json.dump([value.my_data() for value in self.__dict__[key]], f, indent=4)

        # with open('data/systems.json', 'w') as f:
        #     json.dump([system.my_data() for system in self.systems], f, indent=4)
        # with open('data/ships.json', 'w') as f:
        #     json.dump([ship.my_data() for ship in self.ships], f, indent=4)
        # with open('data/locations.json', 'w') as f:
        #     json.dump([location.my_data() for location in self.locations], f, indent=4)
        # with open('data/markets.json', 'w') as f:
        #     json.dump([market.my_data() for market in self.markets], f, indent=4)
        # with open('data/structures.json', 'w') as f:
        #     json.dump([structure.my_data() for structure in self.structures], f, indent=4)
        # with open('data/flightplans.json', 'w') as f:
        #     json.dump([flightplan.my_data() for flightplan in self.flightplans], f, indent=4)

    def fill_from_api(self):
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