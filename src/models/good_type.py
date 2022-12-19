from src.models import Generic
class GoodType(Generic):
    __table__ = 'good_types'
    columns = ['symbol', 'name', 'volumePerUnit']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)