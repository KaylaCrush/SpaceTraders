from src.models.generic import Generic

class Loan(Generic):
    def __init__(self, data, store = None):
        super().__init__(data = data, store = store)
