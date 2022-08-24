from flask import Flask, render_template

from src.display.foliumstarmap import StarMap
import folium
from src.store import Store
from src.models import Ship
import src.api as api


app = Flask(__name__)
store = Store()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ships')
def ships():
    return render_template('ships.html', ships = store.ships)

@app.route('/ships/<id>')
def ship(id):
    return render_template('ship.html', ship = store.get_ship(id))

@app.route('/locations')
def locations():
    return render_template('locations.html', locations = store.locations)

@app.route('/locations/<symbol>')
def location(symbol):
    return render_template('location.html', location = store.get_location(symbol))

@app.route('/locations/<symbol>/market')
def market(symbol):
    return render_template('market.html', market = store.get_market(symbol))

@app.route('/user')
def user():
    return render_template('user.html', user = store.user)

@app.route('/shipyards')
def shipyards():
    return render_template('shipyards.html', shipyards = store.types['shipyards'])

@app.route('/locations/<symbol>/shipyard/<ship_type>')
def purchace_ship(symbol, ship_type):
    response = api.buy_ship(symbol, ship_type)
    Ship(store = store, data = response['ship'])
    return render_template('buy_ship.html', response = response)

@app.route('/ships/<ship_id>/<good>/<quantity>')
def purchace_good(ship_id, good, quantity):
    response = api.purchace_goods(ship_id, good, quantity)
    return render_template('purchace_goods.html', response = response)

@app.route('/starmap')
def starmap():
    stars = StarMap()
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()