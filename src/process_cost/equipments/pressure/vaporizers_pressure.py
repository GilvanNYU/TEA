from .core import PressureFactor, PressureProperties, PressureFactorResult

class VaporizerPressure:
    def __init__(self) -> None:
        self._pressure = PressureFactor([
            PressureProperties((None, 5), (0.0, 0.0, 0.0)),
            PressureProperties((5, 320), (-0.16742, 0.13428, 0.15058))],
                                "barg")

    @property
    def unit(self) -> str:
        return self._pressure.unit
    
    def factor(self, pressure: float) -> PressureFactorResult:
        return self._pressure.factor(pressure)