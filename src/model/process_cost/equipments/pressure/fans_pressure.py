from .core import PressureFactor, PressureProperties, PressureFactorResult

class FanPressure:
    def __init__(self, type: str) -> None:
        if type == 'CentrifugalRadial' or type == 'BackwardCurve':
            self._pressure: PressureFactor = PressureFactor([
                PressureProperties((None, 1), (0.0, 0.0, 0.0)),
                PressureProperties((1, 16), (0.0, 0.20899, -0.0328))],
                "barg")
        else:
            self._pressure: PressureFactor = PressureFactor([
                PressureProperties((None, 1), (0.0, 0.0, 0.0)),
                PressureProperties((1, 4), (0.0, 0.20899, -0.0328))],
                "barg")
   
    @property
    def unit(self) -> str:
        return self._pressure.unit
    
    def factor(self, pressure: float) -> PressureFactorResult:
        return self._pressure.factor(pressure)