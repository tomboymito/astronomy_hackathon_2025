class AstronomicalCalculationError(Exception):
    pass

class NegativeDistanceError(AstronomicalCalculationError):
    def __init__(self, value: float):
        super().__init__(f"Расстояние не может быть отрицательным: {value}")

class InvalidAlbedoError(AstronomicalCalculationError):
    def __init__(self, value: float):
        super().__init__(f"Альбедо должно быть в диапазоне (0, 1]: {value}")