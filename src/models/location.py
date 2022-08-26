from src.models import Generic, LocationTrait
from src.api import get_location_data
from src.orm import build_from_record, save

class Location(Generic):
    __table__ = 'locations'
    api_function = get_location_data
    columns = ['symbol', 'type', 'name', 'x', 'y', 'allowsConstruction']
    primary_keys = ['symbol']

    def __init__(self, **kwargs):
        traits = kwargs.pop('traits', None)
        if traits:
            for trait in traits:
                record = {'location_symbol': kwargs['symbol'], 'trait':trait}
                save(build_from_record(LocationTrait, record))
        super().__init__(**kwargs)