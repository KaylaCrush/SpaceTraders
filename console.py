from src.display import *
from src.dalle import *
from src.api import *

for location in get_system_locations('OE'):
    generate_location_image(location['symbol'])
for ship in get_available_ships():
    generate_ship_image(ship['type'])