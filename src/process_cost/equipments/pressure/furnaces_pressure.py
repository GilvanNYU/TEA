from .core import PressureFactor, PressureProperties, PressureFactorResult

class FurnacePressure:
    def __init__(self, type: str) -> None:
        if type == 'ReformerFurnace':
            self._pressure: PressureFactor = PressureFactor([
                PressureProperties((None, 10), (0.0, 0.0, 0.0)),
                PressureProperties((10, 200), (0.1405,-0.2698, 0.1293))],
                                    "barg")
        elif type == 'PyrolysisFurnace':
            self._pressure: PressureFactor = PressureFactor([
                PressureProperties((None, 10), (0.0, 0.0, 0.0)),
                PressureProperties((10, 200), (0.1017, -0.1957, 0.09403))],
                                    "barg")
        else:
            self._pressure: PressureFactor = PressureFactor([
                PressureProperties((None, 10), (0.0, 0.0, 0.0)),
                PressureProperties((10, 200), (0.1347, -0.2368, 0.1021))],
                                    "barg")

    @property
    def unit(self) -> str:
        return self._pressure.unit
    
    def factor(self, pressure: float) -> PressureFactorResult:
        return self._pressure.factor(pressure)