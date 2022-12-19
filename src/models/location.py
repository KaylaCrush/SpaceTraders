from src.models import Generic
class Location(Generic):
    __table__ = 'locations'
    columns = ['symbol', 'type', 'name', 'x', 'y', 'allowsConstruction']

    def __init__(self, **kwargs):
        super.__init__(**kwargs)