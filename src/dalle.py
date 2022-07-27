#% env REPLICATE_API_TOKEN=5ded05b00c15a89b3112489661b919975e59e8ae
import replicate
from src.api import *
import os

#model = replicate.models.get("borisdayma/dalle-mini")

#model.predict(prompt="a habitable planet called prime")

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

  return f"a {', '.join(traits[0:2])}, sci-fi {data['type'].lower()} called {data['name']}"


def generate_location_image(location_id):
  prompt = descriptive_location_name(location_id)
  file = f'data/img/locations/{location_id}.png'
  model = replicate.models.get("borisdayma/dalle-mini")
  result_url = model.predict(prompt="a habitable planet called prime", n_predictions=1)[0]['image']
  r=requests.get(result_url, allow_redirects=True)
  open(file, 'wb').write(r.content)
    
