import math
from typing import Tuple
from .pressure_factor_result import PressureFactorResult


class PressureProperties:
    def __init__(self, bounds: Tuple[float, float], parameters: Tuple[float, float, float]) -> None:
        self._bounds = (bounds[0] if bounds[0] != None else 0.0,
                        bounds[1] if bounds[1] != None else math.inf)
        self._parameters = parameters

    @property
    def unit(self)-> float:
        return self._unit
    
    @property
    def lower(self)-> float:
        return self._bounds[0]
    
    @property
    def upper(self)-> float:
        return self._bounds[1]
    
    @property
    def parameters(self) -> tuple[float, float, float]:
        return self._parameters
    
    def check_limites(self, pressure: float) -> Tuple[bool,str]:
        if pressure >= self._bounds[0] and pressure <= self._bounds[1]:
            return (True, "OK")
        elif pressure < self._bounds[0]:
            return (False, "Warning - Below minimum pressure")
        else:
            return (False, "Warning - Above maximum pressure",)