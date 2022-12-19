class Cargo():
    __table__ = 'cargo'
    columns = ['ship_id', 'good', 'quantity']

    def __init__(self, **kwargs):
        super.__init__(**kwargs)