from server.src.models.model import Model

class Estimate:
    id: int
    name: str
    # models: list[Model]

    def __init__(self, values: dict):
        for key in values:
            setattr(self, key, values[key])
    