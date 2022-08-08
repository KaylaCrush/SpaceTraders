from src.classes import *
from tests.test_data import *

def test_ship_from_api():
    assert Ship(sample_ship['id']).id == sample_ship['id']

def test_ship_from_file():
    assert Ship(data=sample_ship).id == sample_ship['id']

def test_location_from_api():
    assert Location(sample_location['symbol']).symbol == sample_location['symbol']

def test_location_from_file():
    assert Location(data=sample_location).symbol == sample_location['symbol']

def test_system_from_api():
    assert System(sample_system['symbol']).symbol == sample_system['symbol']

def test_system_from_file():
    assert System(data=sample_system).symbol == sample_system['symbol']

## TODO: get good structure id for this test
# def test_structure_from_api():
    #  assert Structure(sample_structure['id']).id == sample_structure['id']

def test_structure_from_file():
    assert Structure(data=sample_structure).id == sample_structure['id']

def test_market():
    assert Market('OE-PM-TR').location_id == 'OE-PM-TR'

def test_market_from_file():
    assert Market(data=sample_market).location_id == sample_market['location_id']

def test_flightplan_from_api():
    ship = Ship(sample_ship['id'])
    destinations = ['OE-PM-TR', 'OE-PM']
    if ship.has_location():
        if ship.location == destinations[0]:
            flightplan = FlightPlan(ship.id, destinations[1])
        else:
            flightplan = FlightPlan(ship.id, destinations[0])
        assert type(flightplan) == FlightPlan

def test_flightplan_from_file():
    assert FlightPlan(data=sample_flightplan).id == sample_flightplan['id']