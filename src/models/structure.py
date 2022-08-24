from src.models.generic import Generic
from src.api import get_structure_data

class Structure(Generic):
    def __init__(self, structure_id = None, data = None, store = None):
        super().__init__(first_id = structure_id, data = data, data_function=get_structure_data, store = store)