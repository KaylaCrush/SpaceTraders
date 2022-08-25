from src.models import Generic
class Ship():
    __table__ = 'ships'
    columns = ['id', 'location', 'x', 'y', 'spaceAvailable']

    def __init__(self, **kwargs):
        super.__init__(**kwargs)