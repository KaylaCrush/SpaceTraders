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

        if load_from_file and exists('data/systems.json'):
            self.fill_from_file()
        else:
            self.fill_from_api()

        self.save_to_file()

    def fill_from_file(self):
        with open('data/systems.json', 'r') as f:
            self.systems = [System(store = self, data=data) for data in json.load(f)]
        with open('data/ships.json', 'r') as f:
            self.ships = [Ship(store = self, data=data) for data in json.load(f)]
        with open('data/locations.json', 'r') as f:
            self.locations = [Location(store = self, data=data) for data in json.load(f)]
        with open('data/markets.json', 'r') as f:
            self.markets = [Market(store = self, data=data) for data in json.load(f)]
        with open('data/structures.json', 'r') as f:
            self.structures = [Structure(store = self, data=data) for data in json.load(f)]
        with open('data/flightplans.json', 'r') as f:
            self.flightplans = [FlightPlan(store = self, data=data) for data in json.load(f)]

    def save_to_file(self):
        with open('data/systems.json', 'w') as f:
            json.dump([system.my_data() for system in self.systems], f)
        with open('data/ships.json', 'w') as f:
            json.dump([ship.my_data() for ship in self.ships], f)
        with open('data/locations.json', 'w') as f:
            json.dump([location.my_data() for location in self.locations], f)
        with open('data/markets.json', 'w') as f:
            json.dump([market.my_data() for market in self.markets], f)
        with open('data/structures.json', 'w') as f:
            json.dump([structure.my_data() for structure in self.structures], f)
        with open('data/flightplans.json', 'w') as f:
            json.dump([flightplan.my_data() for flightplan in self.flightplans], f)

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