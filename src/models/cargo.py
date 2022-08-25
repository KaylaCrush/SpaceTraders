from src.models import Generic

class Cargo(Generic):
    __table__ = 'cargo'
    columns = ['ship_id', 'good', 'quantity']

    def __init__(self, **kwargs):
            super().__init__(**kwargs)
