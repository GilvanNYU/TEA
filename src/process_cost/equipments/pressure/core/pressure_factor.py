import math
from .pressure_factor_result import PressureFactorResult
from .pressure_properties import PressureProperties

class PressureFactor:
    def __init__(self, properties: list[PressureProperties], unit: str) -> None:
        self._unit = unit
        self._properties = properties
        self._max = PressureProperties((math.inf, math.inf), (None, None, None))
        self._min = PressureProperties((0.0, 0.0), (None, None, None))
        for prop in self._properties:
            self._min = prop if prop.lower < self._min.lower else self._min
            self._max = prop if prop.upper > self._max.upper else self._max
    @property
    def unit(self) -> str:
        return self._unit

    def factor(self, pressure: float) -> PressureFactorResult:
        log_press = math.log(pressure,10)
        for prop in self._properties:
            status = prop.check_limites(pressure)
            if status[0]:
                C1, C2, C3 = prop.parameters
                fp = 10**(C1 + C2*log_press + C3*(log_press**2))
                return PressureFactorResult(value=fp, status=status)
            
        if pressure > self._max.upper:
            C1, C2, C3 = self._max.parameters
            fp = 10**(C1 + C2*log_press + C3*(log_press**2))
            return PressureFactorResult(value=fp, status=self._max.check_limites(pressure))
        else:
            C1, C2, C3 = self._min.parameters
            fp = 10**(C1 + C2*log_press + C3*(log_press**2))
            return PressureFactorResult(value=fp, status=self._min.check_limites(pressure))