from src.api import *
from src.store import *
from src.classes import *

print(get_ship_data(get_ships()[0]['id']).items())