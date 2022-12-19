from src.models import Generic
class LocationTrait(Generic):
    __table__ = 'location_traits'
    columns = ['location_symbol', 'trait']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)