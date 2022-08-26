from src.models import Generic, Cargo
from src.api import get_ship_data
from src.orm import build_from_record, save

class Ship(Generic):
    __table__ = 'ships'
    api_function = get_ship_data
    columns = ['id', 'location', 'x', 'y', 'spaceAvailable']
    primary_keys = ['id']

    def __init__(self, **kwargs):
        cargo = kwargs.pop('cargo', None)
        if cargo:
            for item in cargo:
                item['ship_id'] = kwargs['id']
                save(build_from_record(Cargo, item))
        super().__init__(**kwargs)