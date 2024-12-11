from .core import PressureFactor, PressureProperties, PressureFactorResult

class PumpPressure:

    def __init__(self, type: str) -> None:
        if type == 'Centrifugal':            
            self._pressure = PressureFactor([
                PressureProperties((None, 10), (0.0, 0.0, 0.0)),
                PressureProperties((10, 100), (0.1347, -0.2368, 0.1021))],
                                    "barg")
        else:
            self._pressure = PressureFactor([
                PressureProperties((None, 10), (0.0, 0.0, 0.0)),
                PressureProperties((10, 100), (-0.3935, 0.3957, -0.00226))],
                                    "barg") 
    
    @property
    def unit(self) -> str:
        return self._pressure.unit

    def factor(self, pressure: float) -> PressureFactorResult:
        return self._pressure.factor(pressure)