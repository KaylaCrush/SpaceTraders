from src.models import Generic
from src.api import get_location_data
class Location(Generic):
    __table__ = 'locations'
    api_function = get_location_data
    columns = ['symbol', 'type', 'name', 'x', 'y', 'allowsConstruction']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)