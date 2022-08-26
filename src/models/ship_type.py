from src.models import Generic
class ShipType(Generic):
    __table__ = 'ship_types'
    columns = ['class', 'manufacturer', 'maxCargo', 'plating', 'speed', 'type', 'weapons']
    primary_keys = ['type']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)