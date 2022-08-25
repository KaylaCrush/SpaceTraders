from src.api import *
from tests.test_data import *

def test_make_request():
  url = 'https://api.spacetraders.io/game/status'
  response = {"status": "spacetraders is currently online and available to play"}
  assert make_request(url).json() == response

def test_get_my_status():
  assert get_my_status()['username'] == sample_user['username']

def test_get_money():
  assert type(get_my_money()) == int

def test_get_loans():
  assert type(get_loans()) == list

def test_get_location_data():
  assert get_location_data(sample_location['symbol'])['symbol'] == sample_location['symbol']

def test_get_ships():
  assert type(get_my_ships()) == list

def test_get_ships():
  assert type(get_my_ships()) == list

def test_get_ship_data():
  assert get_ship_data(sample_ship['id'])['id'] == sample_ship['id']

def test_get_system_ship_listings():
  assert type(get_system_ship_listings(sample_system['symbol'])) == list

def test_get_system_flightplans():
  assert type(get_system_flightplans(sample_system['symbol'])) == list

def test_get_system_ships():
  assert type(get_system_ships(sample_system['symbol'])) == list

def test_get_system_data():
  assert get_system_data(sample_system['symbol']) == sample_system

def test_get_available_goods():
  assert type(get_goods_types()) == list

def test_get_available_loans():
  assert type(get_loans_types()) == list

def test_get_available_ships():
  assert type(get_ships_types()) == list

def test_get_available_structures():
  assert type(get_structures_types()) == list

def test_get_available_ships():
  assert type(get_ships_types()) == list