from src.models import Generic
from src.api import get_available_goods
class GoodType(Generic):
    __table__ = 'good_types'
    columns = ['symbol', 'name', 'volumePerUnit']

    def __init__(self, **kwargs):
        super.__init__(**kwargs)