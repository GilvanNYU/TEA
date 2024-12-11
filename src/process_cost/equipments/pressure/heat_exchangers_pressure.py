from .core import PressureFactor, PressureProperties, PressureFactorResult

class HeatExchangerPressure:
    def __init__(self, type: str, tube_only: bool) -> None:
        if type in ['ScrapedWall', 'DoublePipe', 'MultiplePipe']:            
            self._pressure = PressureFactor([
                PressureProperties((None, 40), (0.0, 0.0, 0.0)), 
                PressureProperties((40, 100), (0.6072, -0.9120, 0.3327)),
                PressureProperties((100, 300), (13.1467, -12.6574, 3.0705))],
                                    "barg")
        elif type == 'TeflonTube':
            self._pressure = PressureFactor([
                PressureProperties((None, 15), (0.0, 0.0, 0.0))], "barg")
        elif type in ['FlatPlate', 'SpiralPlate']:
            self._pressure = PressureFactor([
                PressureProperties((None, 19), (0.0, 0.0, 0.0))], "barg")
        elif type == 'AirCooler':
            self._pressure = PressureFactor([
                PressureProperties((None, 10), (0.0, 0.0, 0.0)),
                PressureProperties((10, 100), (-0.1250, 0.15361, -0.02861))],
                                   "barg")
        elif type == 'SpiralTube':
            if tube_only:
                self._pressure = PressureFactor([
                    PressureProperties((None, 150), (0.0, 0.0, 0.0)),
                    PressureProperties((150, 400), (-0.2115, 0.09717, 0.0))],
                                       "barg")
            else:
                self._pressure = PressureFactor([
                    PressureProperties((None, 150), (0.0, 0.0, 0.0)),
                    PressureProperties((150, 400), (-0.4045, 0.1859, 0.0))],
                                       "barg")
        else:
            if tube_only:
                self._pressure = PressureFactor([
                    PressureProperties((None, 5), (0.0, 0.0, 0.0)),
                    PressureProperties((5, 140), (-0.00164, -0.00627, 0.0123))],
                                       "barg")
            else:
                self._pressure = PressureFactor([
                    PressureProperties((None, 5), (0.0, 0.0, 0.0)),
                    PressureProperties((5, 140), (0.03881, -0.11272, 0.08183))],
                                       "barg")
    
    @property
    def unit(self) -> str:
        return self._pressure.unit

    def factor(self, pressure: float) -> PressureFactorResult:
        return self._pressure.factor(pressure)