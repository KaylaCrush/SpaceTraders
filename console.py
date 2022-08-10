from src.api import *
from src.store import *
from src.classes import *

ship_id = get_ships()[0]['id']
make_flightplan(ship_id, 'OE-PM-TR')