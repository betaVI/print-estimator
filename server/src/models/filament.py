class Filament:
    def __init__(self, values: dict) -> None:
        for key in values:
            setattr(self, key, values[key])