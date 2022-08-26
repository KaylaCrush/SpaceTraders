import psycopg2
import src.orm as orm
from src.db import *
from src.models import Ship, ShipType, Cargo, GoodType, Location, LocationTrait, System
import src.api as api
from settings import KNOWN_SYSTEMS

conn = psycopg2.connect(database = 'space_traders', user = 'geekc')
cursor = conn.cursor()

for ship in api.get_my_ships():
    orm.save(orm.build_from_record(Ship, ship))

for system in KNOWN_SYSTEMS:
    orm.save(orm.build_from_record(System, api.get_system_data(system)))
    for location in api.get_system_locations(system):
        orm.save(orm.build_from_record(Location, location))

for good in api.get_goods_types():
    orm.save(orm.build_from_record(GoodType, good))
    
for ship in api.get_ships_types():
    orm.save(orm.build_from_record(ShipType, ship))