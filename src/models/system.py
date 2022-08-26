from src.models import Generic
from src.api import get_system_data
class System(Generic):
    __table__ = 'systems'
    primary_keys = ['symbol']
    api_function = get_system_data
    columns = ['symbol', 'name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)