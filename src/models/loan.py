from src.models.generic import Generic
from src.api import *

class Loan(Generic):
    def __init__(self, data, store = None):
        super().__init__(data = data, store = store)
