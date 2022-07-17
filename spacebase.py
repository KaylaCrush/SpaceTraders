import requests
import time
import math
import pickle
import folium
from branca.element import Figure

"""
Constants:
"""

USERNAME = 'crushbone'
TOKEN    = 'e5cafd30-73e6-4d85-bd1d-32c1bbc6bace'
FILE     = "drive/MyDrive/Colab Notebooks/starchart.pkl"

"""
Temporarily Useful Variables:
"""

my_ship_id = 'cl55thau617774315s68iz3fpjj'
cargo_ship_id = 'cl58tw4u525771615s6bnh9pips'
starting_system = "OE"

"""
URLs:
"""

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

"""
Functions:
"""

## =====API CALLS===== ##
def make_request(url, params={}, type='GET'):
  time.sleep(1) # Delay to avoid disconnect for spamming
  headers = {"Authorization": f"Bearer {TOKEN}"}
  if type == 'GET':
    response = requests.get(url, headers=headers, params=params)
  elif type == 'POST':
    response = requests.post(url, headers=headers, params=params)
  elif type == 'PUT':
    response = requests.put(url, headers=headers, params=params)
  elif type == 'DELETE':
    response = requests.delete(url, headers=headers, params=params)
  response.raise_for_status() # Errors out if a request is unsuccessful
  return response

## these functions cover (almost?) all the API requests at https://api.spacetraders.io/

# PLAYER INFO
def get_my_status(params={}):
  return make_request(myInfo_url, params=params).json()['user']

def get_money():
  return make_request(myInfo_url).json()['user']['credits']

# FLIGHTPLAN
def get_flightplan(flightPlan_id, params={}):
  return make_request(f'{flightplan_url}/{flightPlan_id}', params=params).json()['flightPlan']
  
def make_flightplan(ship_id, destination):
  return make_request(f'{flightplan_url}', params={'shipId':ship_id, 'destination':destination}, type="POST").json()['flightPlan']

# LOANS
def get_loans():
  return make_request(url= f'{loans_url}').json()['loans']

def pay_loan(loan_id):
  return make_request(f'{loans_url}/{loan_id}', type="PUT").json()

def take_loan(loan_type):
  return make_request(f'{loans_url}', params={'type':loan_type}, type="POST").json()

# LOCATIONS
def get_location_data(location_id, params={}):
  return make_request(f'{location_url}/{location_id}', params=params).json()['location']

def get_market_data(location_id, params={}):
  return make_request(f'{location_url}/{location_id}/marketplace', params=params).json()['marketplace']

def get_ships(location_id, params={}):
  return make_request(f'{location_url}/{location_id}/ships', params=params).json()['ships']

def get_structures(location_id, params={}):
  return make_request(f'{location_url}/{location_id}/structures', params=params).json()['structures']

# COMMERCE
def purchace_goods(ship_id, good, quantity):
  return make_request(f'{purchace_url}', params={'shipId':ship_id,'quantity':quantity,'good':good}, type='POST').json()

def sell_goods(ship_id, good, quantity):
  return make_request(f'{sell_url}', param={'shipId':ship_id,'quantity':quantity,'good':good}, type='POST').json()

def fuel_ship(ship_id,fuel_amount): #
  return purchace_goods(f'{ship_id}', 'FUEL', fuel_amount).json()

# SHIPS
def buy_ship(location, type):
  return make_request(f'{myShips_url}',params = {'location': location, 'type': type}, type = "POST").json()

def get_ships(params={}):
  return make_request(myShips_url, params=params).json()['ships']

def get_ship_data(ship_id, params={}):
  return make_request(f'{myShips_url}/{ship_id}', params=params).json()['ship']

def jettison_ship_cargo(ship_id, good, quantity):
  return make_request(f'{myShips_url}/{ship_id}/jettison', params = {'shipId':ship_id, 'good':good, 'quantity':quantity}, type="POST").json()

def scrap_ship(ship_id):
  return make_request(f'{myShips_url}/{ship_id}', type = "DELETE").json()

def transfer_ship_cargo(from_ship_id, to_ship_id, good, quantity):
  return make_request(f'{myShips_url}/{from_ship_id}', params = {'toShipId':to_ship_id, 'good': good,'quantity':quantity}, type ="POST").json()

#STRUCTURES
def get_structure_data(structure_id):
  return make_request(f'{struct_url}/{structure_id}')['structure']

def get_my_structure_data(structure_id):
  return make_request(f'{my_struct_url}/{structure_id}')['structure']

def get_my_structures():
  return make_request(f'{my_struct_url}')['structures']

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
def get_available_goods(params={}):
  return make_request(f'{types_url}/goods', params=params).json()['goods']

def get_available_loans(params={}):
  return make_request(f'{types_url}/loans').json()['loans']

def get_available_structures(params={}):
  return make_request(f'{types_url}/structures').json()['structures']

def get_available_ships(params={}):
  return make_request(f'{types_url}/ships').json()['ships']

#USERS
def claim_username(username):
  response = make_request(f'https://api.spacetraders.io/users/{username}/claim').json()
  [print(key,':',value) for key, value in response.items()]
  return print()

def warp_jump(ship_id):
  return make_request(f'https://api.spacetraders.io/my/warp-jumps', params={'shipId':ship_id}).json()['flightPlan']


## ADDITIONAL HELPER FUNCTIONS
# writes a starchart's saved system data to file
def save_starchart(starchart):
  a_file = open(FILE, "wb")
  pickle.dump(starchart.getLocationsData(), a_file)
  a_file.close()

# creates a new starchart from a saved file
def load_starchart():  
  a_file = open(FILE, "rb")
  output = pickle.load(a_file)
  a_file.close()
  return StarChart(output)

# distance between two [x,y] points
def distance_between(xy1, xy2):
  x = xy1[0]-xy2[0]
  y = xy1[1]-xy2[1]
  return math.hypot(x, y)

def ships_present(location):
  for ship in get_ships():
    if ship['location'] == location:
      return True
  return False

#Classes:

#--ENTITY--
#Entities include locations, ships, markets, loans, purchace and sell orders, structures, and systems
#subsidiary windows: list of ongoing flights, database of known systems and markets, list of ships in fleet, player info
#they all have in common that they can display a window about themselves.
#they all have a title, an id, and data
#todo = just merge with Localized_Entity??

class Entity(): 
  def __init__(self, id, data = {}, url = ""):
    self.id = id
    self.data = data
    self.url = url
  
  def getId(self):                return self.id
  def getData(self):              return self.data
  def getKey(self, key):          return self.getData()[key]

  def setData(self, newData):     self.data = newData
  def updateData(self, newData):  self.data.append(newData)

# --LOCALIZED ENTITY--
#A Localized Entity is just an entity with an x and y coordinate in space
#afaik, that just means ships and planet(oids)

class Localized_Entity(Entity):
  def __init__(self, id, data = {}, url=""):
    super().__init__(id=id, data=data, url=url)

  def getX(self):  return self.data['x']
  def getY(self):  return self.data['y']
  def getXY(self): return [self.getX(), self.getY()]

  # calculate distance between self and either...
  # another Localized_Entity object
  def distanceTo(self, localized_entity):
    return distance_between(self.getXY(), localized_entity.getXY())

  # a given [x,y] coordinate
  def distanceToXY(self, xy):
    return distance_between(self.getXY(), xy)

  # a given planet id
  def distanceToPlanet(self, planet_id):
    data = get_location_data(planet_id)
    return self.distanceToXY([data['x'],data['y']])

  # a given ship id
  def distanceToShip(self, ship_id):
    data = get_ship_data(ship_id)
    return self.distanceToXY([data['x'],data['y']])

#====================================LOCATION============================================
#This class describes a place a ship can travel to - a moon, planet, gas giant, wormhole, etc
#
class Location(Localized_Entity):
  def __init__(self, location_id):
    url=f"{location_url}/{location_id}"
    data= get_location_data(location_id)
    super().__init__(
      id = location_id,
      url = url,
      data=data)
    self.has_market_data = False
    self.market_url=f"{location_url}/{self.getId()}/marketplace"
    self.update_markets()

  # constant, no call
  def allowsConstruction(self): return self.getKey('allowsConstruction')
  def getName(self):            return self.getKey('name')
  def getTraits(self):          return self.getKey('traits')
  def getType(self):            return self.getKey('type')
    
  # variable, call
  def getDockedShips(self): return get_system_ships(self.getId())['ships']

  # market data handling
  def getMarketData(self):
    self.update_markets()
    if self.hasMarketData():
      return self.getData()['marketplace']
    else:
      return {}
  
  def hasMarketData(self):
    return self.has_market_data

  def update_markets(self):
    if self.shipsPresent():
      self.data['marketplace'] = (make_request(self.market_url).json()['marketplace'])
      self.has_market_data=True
  
  #returns true if player has ships in the system
  def shipsPresent(self):
    for ship in get_ships():
      if ship['location'] == self.getId():
        return True
    return False

  # theoretical future version of the same function
  def fleetPresent(self, fleet):
    return len(fleet.getShipsAtLocation(self.getId())) > 0

#=====================================SHIP===============================================
class Ship(Localized_Entity):
  def __init__(self, ship_id):
    url = f'{myShips_url}/{ship_id}',
    data = get_ship_data(ship_id)

    super().__init__(
      id = ship_id,
      url = url,
      data=data
    )

    self.name = f'{self.getManufacturer()} {self.getType()}'
    self.last_flightplan = {}

  def update(self):
    self.data = get_ship_data(self.getId())

  # constant ship values (these do not call the server)
  def getLoadingSpeed(self): return self.getKey('loadingSpeed')
  def getManufacturer(self): return self.getKey('manufacturer')
  def getMaxCargo(self):     return self.getKey('maxCargo')
  def getPlating(self):      return self.getKey('plating')
  def getSpeed(self):        return self.getKey('speed')
  def getType(self):         return self.getKey('type')
  def getWeapons(self):      return self.getKey('weapons')

  # variable ship values (these DO call the server)
  def getCargo(self): return get_ship_data(self.getId())['cargo']

  def getFuel(self): # return fuel, if the ship has any, or returns 0
    if 'FUEL' in self.getCargo().keys():
      return self.getKey('cargo')['FUEL']['quantity']
    return 0

  def getLocation(self):
    return get_ship_data(self.getId())['location']

  def getSpaceAvailable(self):
    return get_ship_data(self.getId())['spaceAvailable']
    
  #ship controls
  def sellGoods(self, good, quantity):
    return sell_goods(self.getId,good,quantity)

  def buyGoods(self, good, quantity):
    if quantity > self.getLoadingSpeed():
      self.buyGoods(good, self.getLoadingSpeed())
      quantity = quantity-self.getLoadingSpeed()
    return purchace_goods(self.getId(),good,quantity)

  def goTo(self, location):
    self.last_flightplan = make_flightplan(self.getId(), location)
    return self.last_flightplan

#======================================FLEET==================================
class Fleet():
  def __init__(self):
    self.ships_list=[]
    self.update()
  
  def update(self):
    self.ships_data = get_ships()
    for ship in self.ships_data:
      if ship['id'] not in self.getShipIds():
        self.ships_list.append(Ship(ship['id']))

  def getShips(self):
    return self.ships_list()

  def getShipIds(self):
    return [ship.getId() for ship in self.getShips()]

  def getShipsAtLocation(self, location_id):
    return [ship for ship in self.getShips() if ship.getLocation() == location_id]

  def getShipById(self, ship_id):
    return [ship for ship in self.getShips() if ship.getId() == ship_id][0]

#======================================STARCHART================================
#Holds data about known systems

class StarChart():
  def __init__(self, *args):
    starting_system ='OE'
    if len(args) == 0:
      self.locations_data = get_system_locations(starting_system) 
    if len(args) == 1:
      self.locations_data = args[0]

    self.system_ids = [location['symbol'] for location in self.locations_data]
    self.locations_dict = {system_id:Location(system_id) for system_id in self.system_ids}

  #returns a list of the [x,y] coordinates of every location in the system
  def getCoords(self):
    return [location.getXY() for location in self.getLocationsList()]

  #returns the locations data in dictionary form
  def getLocationsData(self):
    return self.locations_data

  #returns the locations data in Location form
  def getLocationsList(self):
    return self.locations_dict.values()

  # returns a Locatoin by system id
  def getLocation(self, system_id):
    return self.locations_dict[system_id]
  
  # returns a list of all system id's in the starchart
  def getSystemIds(self): return self.system_ids

##======================================TRADE ROUTES===========================
# trade route class
# holds a list of locations and goods to buy and sell
# planets = {"OE-PM": {"BUY": "", "SELL":"METALS"}, "OE-PM-TR": {"BUY": "METALS", "SELL":""}}
class TradeRoute():
  def __init__(self, route_dict):
    pass

##======================================STRUCTURES???==================================

# %% FRIGGIN DISPLAYS
# 

## STAR MAP FUNCTIONS
# Given a StarChart, displays a Folium map of the locations in the system
class StarMap():
  def __init__(self, starchart):
    self.starfield_url="http://paulbourke.net/miscellaneous/astronomy/8192x4096.png"
    self.figure_size=800
    self.icon_ids = {'PLANET':'fa-globe', 'MOON':'fa-moon-o', 'ASTEROID':'fa-cog', 'GAS_GIANT':'fa-circle-o', 'WORMHOLE':'fa-recycle'}
    self.icon_colors = {'PLANET':'lightblue', 'MOON':'beige', 'ASTEROID':'gray', 'GAS_GIANT':'lightgreen', 'WORMHOLE':'pink'}
  
    self.starchart = starchart
   
    self.oas = self.getOffsetAndScale()
    self.fig = Figure(width=self.figure_size,height=self.figure_size)

  # functions to normalize coordinates for displaying with the star map function
  def getOffsetAndScale(self):
    coords=self.starchart.getCoords()
    x_max = max([coord[0] for coord in coords])
    x_min = min([coord[0] for coord in coords])
    y_max = max([coord[1] for coord in coords])
    y_min = min([coord[1] for coord in coords])
    x_offset = (x_max+x_min)/2 
    y_offset = (y_max+y_min)/2

    x_distance = abs(x_max-x_min)
    y_distance = abs(y_max-y_min)
    scale=(.25*self.figure_size)/max([x_distance, y_distance])

    return[x_offset,y_offset,scale]
  
  def normalizeCoord(self, coord):
    x_offset = self.oas[0]
    y_offset = self.oas[1]
    scale = self.oas[2]
    x = (coord[0]-x_offset)*scale
    y = (coord[1]-y_offset)*scale
    return [x,y]

  def generate_starmap_label(self, location):
    location_details=f'''{location.getType().title()} {location.getId()}: "{location.getName()}" '''
    trait_details = '<br>'.join([" ".join(trait.split('_')).title() for trait in location.getTraits()])
    if location.hasMarketData():
      market_data = location.getMarketData()
      goods_string = "<br>".join([f"""{' '.join(good['symbol'].split('_')).title()}:<br>&emsp;{good['quantityAvailable']} Available<br> &emsp;p/s price: {good['purchasePricePerUnit']}/{good['sellPricePerUnit']}<br>""" for good in market_data])
      market_details = f"<br><center>Market Report:</center><br>{goods_string}"
    else:
      market_details = ""
    return f'<center>{location_details}<br>{trait_details}</center>{market_details}'

  def draw_starmap(self):
    m= folium.Map(crs='Simple', zoom_control=False, tiles=None)
    
    for location in self.starchart.getLocationsList():
      html = self.generate_starmap_label(location)
      html_lines = html.count("<br>")
      frame_height = 30+(20*(html_lines))
      iframe = folium.IFrame(html,height=frame_height,width=275)

      popup = folium.Popup(iframe, max_width=700)

      coord=self.normalizeCoord(location.getXY())
      icon = self.icon_ids[location.getType()]
      icon_color = self.icon_colors[location.getType()]
 
      folium.Marker(coord,
                    tooltip=location.getName(), 
                    popup=popup,
                    icon=folium.Icon(color='black', icon_color=icon_color, icon=icon, prefix='fa')
                    ).add_to(m)

    overlay_size = self.figure_size

    starmap_overlay = folium.raster_layers.ImageOverlay(bounds=[[-overlay_size,-overlay_size],[overlay_size,overlay_size]],
                                                        image=self.starfield_url).add_to(m)
    self.fig.add_child(m)
    return m


# generates a descriptive text string from a location, to be fed into dall e
def descriptive_location_name(location_id):
  data = get_location_data(location_id)

  abundant_traits = []
  average_traits = []
  some_traits = []

  traits_dict = {
      "METAL_ORES":"metalic",
      "NATURAL_CHEMICALS":"toxic",
      "RARE_METAL_ORES":"crystaline",
      "TECHNOLOGICAL_RUINS":"ancient alien",
      "ARABLE_LAND":"earthlike",
      "HELIUM_3":""}

  for trait in data['traits']:
    if "ABUNDANT" in trait:
      abundant_traits.append(traits_dict[trait.partition('_')[2]])
    elif "SOME" in trait:
      some_traits.append(traits_dict[trait.partition('_')[2]])
    else:
      average_traits.append(traits_dict[trait])

  traits = abundant_traits + average_traits + some_traits

  weights=([10] * len(abundant_traits))+([5] * len(average_traits))+([1]*len(some_traits))
  
  print(traits)
  print(weights)

  return f"a {' '.join(traits[0:2])} {data['type'].lower()} called {data['name']}"
