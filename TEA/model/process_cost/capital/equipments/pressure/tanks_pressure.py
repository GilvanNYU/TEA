from .core import PressureFactor, PressureProperties, PressureFactorResult

class TankPressure:
    def __init__(self) -> None:
        self._pressure = PressureFactor([
            PressureProperties((None, 10), (0.0, 0.0, 0.0)),
            PressureProperties((10, 150), (0.1578, -0.2992, 0.1413)) ],
                                "barg")
    
    @property
    def unit(self) -> str:
        return self._pressure.unit
    
    def factor(self, pressure: float) -> PressureFactorResult:
        return self._pressure.factor(pressure)