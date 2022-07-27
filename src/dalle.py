#% env REPLICATE_API_TOKEN=5ded05b00c15a89b3112489661b919975e59e8ae
import replicate
from src.api import *
import os

#model = replicate.models.get("borisdayma/dalle-mini")

#model.predict(prompt="a habitable planet called prime")

os.environ["REPLICATE_API_TOKEN"]="5ded05b00c15a89b3112489661b919975e59e8ae"


def descriptive_ship_name(ship_type):
  ships = get_available_ships()
  ship = [ship for ship in ships if ship['type']==ship_type][0]
  shipstring = "a "
  match ship['class']:
    case 'MK-I':
      shipstring = shipstring + "run-down "
    case 'MK-II':
      shipstring = shipstring + "run-of-the-mill "
    case 'MK-III':
      shipstring = shipstring + "high-tech "
  
  if ship['speed'] > 3:
    shipstring = shipstring + "fast "
  if ship['weapons']>5:
    shipstring = shipstring + "heavily-armed "
  shipstring = shipstring + ship['manufacturer'] + " space ship"
  return shipstring




def descriptive_location_name(location_id):
  data = get_location_data(location_id)

  if data['type'] == "WORMHOLE":
    location_string = "a mysterious worhmole designated " + location_id
  else:
    traits=[]

    traits_dict = {
        "METAL_ORES":"metalic",
        "NATURAL_CHEMICALS":"toxic",
        "RARE_METAL_ORES":"crystaline",
        "TECHNOLOGICAL_RUINS":"ancient alien",
        "ARABLE_LAND":"earthlike",
        "HELIUM_3":""}

    for trait in data['traits']:
      if "ABUNDANT" in trait or "SOME" in trait:
        traits.append(traits_dict[trait.partition('_')[2]])
      else:
        traits.append(traits_dict[trait])

    location_string = f"a {' '.join(traits[0:2])} {data['type'].lower()} designated {data['name']}"
  return location_string


def generate_location_image(location_id):
  prompt = descriptive_location_name(location_id)
  file = f'data/img/locations/{location_id}.png'
  model = replicate.models.get("borisdayma/dalle-mini")
  result_url = model.predict(prompt=prompt, n_predictions=1)[0]['image']
  r=requests.get(result_url, allow_redirects=True)
  open(file, 'wb').write(r.content)
    
def generate_ship_image(ship_type):
  prompt = descriptive_ship_name(ship_type)
  file = f'data/img/ships/{ship_type}.png'
  model = replicate.models.get("borisdayma/dalle-mini")
  result_url = model.predict(prompt=prompt, n_predictions=1)[0]['image']
  r=requests.get(result_url, allow_redirects=True)
  open(file, 'wb').write(r.content)