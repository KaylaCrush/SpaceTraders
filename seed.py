import psycopg2
import src.orm as orm
from src.db import *
from src.models import Ship, ShipType, Cargo, GoodType, Location, LocationTrait
import src.api as api

conn = psycopg2.connect(database = 'space_traders', user = 'geekc')
cursor = conn.cursor()


for ship in api.get_ships():
    orm.save(ship, conn, cursor)




# famiglia = Venue(foursquare_id = '1234', name = 'La Famiglia', price = 1,
#         rating = 2, likes = 3, menu_url = 'lafamig.com')
# mogador = Venue(foursquare_id = '5678', name = 'Cafe Mogador', 
#         price = 3, rating = 4, likes = 15, menu_url = 'cafemogador.com')
# save(famiglia, conn, cursor)
# save(mogador, conn, cursor)

# pizza = Category(name = 'Pizza')
# italian = Category(name = 'Italian')

# save(pizza, conn, cursor)
# save(italian, conn, cursor)
