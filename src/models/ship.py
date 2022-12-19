from src.models import Generic
from src.api import get_ship_data
class Ship():
    __table__ = 'ships'
    api_function = get_ship_data
    columns = ['id', 'location', 'x', 'y', 'spaceAvailable']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)