## ship roles
# scout - goes to a place and sits there so i can gather up to date market data
# trader - flies a trade route from location to location
#
# ships can be assigned roles
# ships with roles will be checked for tasks during the main loop

# roles are assigned to ships via the ship's role attribute
# ships should have a function to check fuel levels, calculate fuel to destination, buy the fuel, and create the fligtplan
# trade routes should be able to determine total fuel required by a route and buy as much fuel as needed at the cheapest port

from src.models.ship import Ship

class Role:
    def __init__(self, role_name):
        self.name = role_name

    
