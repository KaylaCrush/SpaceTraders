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
            self.systems = [System(data=data) for data in json.load(f)]
        with open('data/ships.json', 'r') as f:
            self.ships = [Ship(data=data) for data in json.load(f)]
        with open('data/locations.json', 'r') as f:
            self.locations = [Location(data=data) for data in json.load(f)]
        with open('data/markets.json', 'r') as f:
            self.markets = [Market(data=data) for data in json.load(f)]
        with open('data/structures.json', 'r') as f:
            self.structures = [Structure(data=data) for data in json.load(f)]
        with open('data/flightplans.json', 'r') as f:
            self.flightplans = [FlightPlan(data=data) for data in json.load(f)]

    def save_to_file(self):
        with open('data/systems.json', 'w') as f:
            json.dump([system.__dict__ for system in self.systems], f)
        with open('data/ships.json', 'w') as f:
            json.dump([ship.__dict__ for ship in self.ships], f)
        with open('data/locations.json', 'w') as f:
            json.dump([location.__dict__ for location in self.locations], f)
        with open('data/markets.json', 'w') as f:
            json.dump([market.__dict__ for market in self.markets], f)
        with open('data/structures.json', 'w') as f:
            json.dump([structure.__dict__ for structure in self.structures], f)
        with open('data/flightplans.json', 'w') as f:
            json.dump([flightplan.__dict__ for flightplan in self.flightplans], f)

    def fill_from_api(self):
        for system_id in KNOWN_SYSTEMS:
            self.systems.append(System(system_id))
        for ship in get_ships():
            self.ships.append(Ship(ship['id']))
        for system_id in KNOWN_SYSTEMS:
            for location in get_system_locations(system_id):
                self.locations.append(Location(location['symbol'])) 
        for ship in self.ships:
            if ship.has_location():
                self.markets.append(Market(ship.location))
        for structure in get_my_structures():
            self.structures.append(Structure(structure['id']))