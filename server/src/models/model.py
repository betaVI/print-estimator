class Model:
    def __init__(self, values: dict):
        for key in values:
            setattr(self, key, values[key])