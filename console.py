from src.display import *
from src.dalle import *
import os
os.environ["REPLICATE_API_TOKEN"]="5ded05b00c15a89b3112489661b919975e59e8ae"
for location in get_system_locations('OE'):
    print(descriptive_location_name(location['symbol']))