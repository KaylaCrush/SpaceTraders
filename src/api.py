import time
import requests
from settings import TOKEN

base_url      = 'https://api.spacetraders.io'
status_url    = f'{base_url}/game/status'
struct_url    = f'{base_url}/structures'
system_url    = f'{base_url}/systems'
location_url  = f'{base_url}/locations'
types_url     = f'{base_url}/types'
my_url        = f'{base_url}/my'
loans_url     = f'{my_url}/loans'
myShips_url   = f'{my_url}/ships'
myInfo_url    = f'{my_url}/account'
purchace_url  = f'{my_url}/purchase-orders'
sell_url      = f'{my_url}/sell-orders'
flightplan_url= f'{my_url}/flight-plans'
my_struct_url = f'{my_url}/structures'


# ## =====API CALLS===== ##
def make_request(url, params={}, req_type='GET', delay=0.0):
  time.sleep(delay)
  headers = {"Authorization": f"Bearer {TOKEN}"}
  
  match req_type:
    case 'GET':
      response = requests.get(url, headers=headers, params=params)
    case 'POST':
      response = requests.post(url, headers=headers, params=params)
    case 'PUT':
      response = requests.put(url, headers=headers, params=params)
    case 'DELETE':
      response = requests.delete(url, headers=headers, params=params)
  
  if response.status_code == 429: # Too Many Requests
    return make_request(url, params, req_type, delay+.01)
    
  response.raise_for_status() # Errors out if a request is unsuccessful
  return response


## these functions cover (almost?) all the API requests at https://api.spacetraders.io/

# PLAYER INFO
def get_my_status(params={}):
  return make_request(myInfo_url, params=params).json()['user']

def get_my_money():
  return make_request(myInfo_url).json()['user']['credits']

# FLIGHTPLAN
def get_flightplan(flightPlan_id, params={}):
  return make_request(f'{flightplan_url}/{flightPlan_id}', params=params).json()['flightPlan']
  
def make_flightplan(ship_id, destination):
  return make_request(f'{flightplan_url}', params={'shipId':ship_id, 'destination':destination}, req_type="POST").json()['flightPlan']

# LOCATIONS
def get_location_data(location_id, params={}):
  return make_request(f'{location_url}/{location_id}', params=params).json()['location']

def get_market_data(location_id, params={}):
  return make_request(f'{location_url}/{location_id}/marketplace', params=params).json()['marketplace']

def get_location_ships(location_id, params={}):
  return make_request(f'{location_url}/{location_id}/ships', params=params).json()['ships']

def get_location_structures(location_id, params={}):
  return make_request(f'{location_url}/{location_id}/structures', params=params).json()['structures']

# COMMERCE
def purchace_goods(ship_id, good, quantity):
  return make_request(f'{purchace_url}', params={'shipId':ship_id,'quantity':quantity,'good':good}, req_type='POST').json()

def sell_goods(ship_id, good, quantity):
  return make_request(f'{sell_url}', param={'shipId':ship_id,'quantity':quantity,'good':good}, req_type='POST').json()

# SHIPS
def buy_ship(location, type):
  return make_request(f'{myShips_url}',params = {'location': location, 'type': type}, req_type = "POST").json()

def get_my_ships(params={}):
  return make_request(myShips_url, params=params).json()['ships']

def get_ship_data(ship_id, params={}):
  return make_request(f'{myShips_url}/{ship_id}', params=params).json()['ship']

def jettison_ship_cargo(ship_id, good, quantity):
  return make_request(f'{myShips_url}/{ship_id}/jettison', params = {'shipId':ship_id, 'good':good, 'quantity':quantity}, req_type="POST").json()

def scrap_ship(ship_id):
  return make_request(f'{myShips_url}/{ship_id}', req_type = "DELETE").json()

def transfer_ship_cargo(from_ship_id, to_ship_id, good, quantity):
  return make_request(f'{myShips_url}/{from_ship_id}', params = {'toShipId':to_ship_id, 'good': good,'quantity':quantity}, req_type ="POST").json()

#STRUCTURES
def get_structure_data(structure_id):
  return make_request(f'{struct_url}/{structure_id}').json()['structure']

def get_my_structures():
  return make_request(f'{my_struct_url}').json()['structures']

def create_structure(location_id, structure_type):
  return make_request(f'{my_struct_url}', params = {'location': location_id, 'type': structure_type}).json()['structure']

def deposit_goods_to_owned_structure(structure_id, ship_id, good, quantity):
  return make_request(f'{my_struct_url}/deposit', params = {'structureId': structure_id, 'shipId': ship_id, 'good': good, 'quantity': quantity}).json()

def deposit_goods_to_public_structure(structure_id, ship_id, good, quantity):
  return make_request(f'{struct_url}/{structure_id}/deposit', params = {'structureId': structure_id, 'shipId': ship_id, 'good': good, 'quantity': quantity}).json()

def transfer_goods_from_owned_structure(structure_id, ship_id, good, quantity):
  return make_request(f'{my_struct_url}/transfer', params = {'structureId': structure_id, 'shipId': ship_id, 'good': good, 'quantity': quantity}).json()

#SYSTEMS
def get_system_ship_listings(system_id, params={}):
  return make_request(f'{system_url}/{system_id}/ship-listings', params=params).json()['shipListings']

def get_system_flightplans(system_id, params ={}):
  return make_request(f'{system_url}/{system_id}/flight-plans', params=params).json()['flightPlans']

def get_system_ships(system_id, params={}):
  return make_request(f'{system_url}/{system_id}/ships', params=params).json()['ships']

def get_system_locations(system_id, params={}):
  return make_request(f'{system_url}/{system_id}/locations', params=params).json()['locations']

def get_system_data(system_id, params={}):
  return make_request(f'{system_url}/{system_id}', params = params).json()['system']

#TYPES
def get_goods_types(params={}):
  return make_request(f'{types_url}/goods', params=params).json()['goods']

def get_loans_types(params={}):
  return make_request(f'{types_url}/loans').json()['loans']

def get_structures_types(params={}):
  return make_request(f'{types_url}/structures').json()['structures']

def get_ships_types(params={}):
  return make_request(f'{types_url}/ships').json()['ships']

#USERS
def claim_username(username):
  response = make_request(f'https://api.spacetraders.io/users/{username}/claim').json()
  [print(key,':',value) for key, value in response.items()]
  return print()

def warp_jump(ship_id):
  return make_request(f'https://api.spacetraders.io/my/warp-jumps', params={'shipId':ship_id}).json()['flightPlan']
