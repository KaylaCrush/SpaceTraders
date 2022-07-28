from src.api import *

def nice_location_name(location):
  return f""" {location['type'].title()} {location['symbol']}: "{location['name']}" """