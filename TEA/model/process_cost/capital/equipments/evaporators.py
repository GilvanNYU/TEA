from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, EquipmentCost
from .pressure import EvaporatorPressure

@dataclass(frozen=True)
class EvaporatorProperties:
    """
    pressure (barg) - Operating pressure
    """
    class Material(Enum):
        CarbonSteel = {'ForcedCirculation': 2.93, 'FallingFilm': 2.23, 'AgitatedFilm': 2.23, 'ShortTube': 2.93, 'LongTube': 2.93}
        CuAlloy = {'ForcedCirculation': 3.68, 'FallingFilm': 2.8, 'AgitatedFilm': 2.8, 'ShortTube': 3.68, 'LongTube': 3.68}
        StainlessSteel = {'ForcedCirculation': 5.08, 'FallingFilm': 4.00, 'AgitatedFilm': 4.0, 'ShortTube': 5.08, 'LongTube': 5.08}
        NiAlloy = {'ForcedCirculation': 9.68, 'FallingFilm': 7.56, 'AgitatedFilm': 7.56, 'ShortTube': 9.68, 'LongTube': 9.68}
        Titanium = {'ForcedCirculation': 14.56, 'FallingFilm': 11.32, 'AgitatedFilm': 11.32, 'ShortTube': 14.56, 'LongTube': 14.56}
    
    class Model(Enum):
        ForcedCirculation = { 'min_size': 5.0, 'max_size': 1000.0, 'data': (5.0238, 0.3475, 0.0703), 'unit':'m2' }
        FallingFilm = { 'min_size': 50.0, 'max_size': 500.0, 'data': (3.9119, 0.8627, -0.0088), 'unit':'m2' }
        AgitatedFilm = { 'min_size': 0.5, 'max_size': 5.0, 'data': (5.0000, 0.1490, -0.0134), 'unit':'m2' }
        ShortTube = { 'min_size': 10.0, 'max_size': 100.0, 'data': (5.2366, -0.6572, 0.3500), 'unit':'m2' }
        LongTube = { 'min_size': 100.0, 'max_size': 10000.0, 'data': (4.6420, 0.3698, 0.0025), 'unit':'m2' }

    material: Material = Material.CarbonSteel
    model : Model = Model.ForcedCirculation
    pressure: float = 0


class EvaporatorCost(EquipmentCost):
    def __init__(self, properties: EvaporatorProperties) -> None:
        self._props = properties
        self._pressure = EvaporatorPressure()
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of evaporator\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(area, CEPCI)        

    def bare_module(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of evaporator\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._props.material.value[self._props.model.name]
        Fp = self._pressure.factor(self._props.pressure)
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp.value)

    def total_module(self, area: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of evaporator\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(area, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))