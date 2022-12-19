class Generic():
    def __init__(self, **kwargs):
        # for key in kwargs.keys():
        #     if key not in self.columns:
        #         raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            if k in self.columns:
                setattr(self, k, v)