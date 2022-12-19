from src.models.generic import Generic
class Transaction(Generic):
    def __init__(self, transaction_type:str, data, store = None):
        data['transaction_type'] = transaction_type
        super().__init__(data = data, store = store)
