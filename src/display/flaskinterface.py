from flask import Flask, render_template, send_from_directory
from src.store import *
app = Flask(__name__)
from markupsafe import escape
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
    response = buy_ship(symbol, ship_type)
    Ship(store = store, data = response['ship'])
    return render_template('buy_ship.html', response = response)

# @app.route('/images/<image_path>')
# def image(image_path):
#         return send_from_directory(
#         app.config['IMAGE_FOLDER'], image_path, as_attachment=True
#     )