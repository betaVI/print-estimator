from src.models.model import Model

class Estimate:
    id: int
    name: str
    # models: list[Model]

    def __init__(self, values: dict):
        for key in values:
            if key == 'models':
                models = []
                for item in values[key]:
                    if type(item) == Model:
                        models.append(item)
                    else:
                        models.append(Model(item))
                setattr(self, key, models)
            else:
                setattr(self, key, values[key])
    