from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

@dataclass(frozen=True)
class ScreenProperties:
    class Model(Enum):
        DSM = { 'min_size': 0.3, 'max_size': 6.0, 'data': (3.8050, 0.5856, 0.2120), 'unit':'m2', 'Fbare': 1.34 }
        Rotary = { 'min_size': 0.3, 'max_size': 15.0, 'data': (4.0485, 0.1118, 0.3260), 'unit':'m2', 'Fbare': 1.34 }
        Stationary = { 'min_size': 2.0, 'max_size': 11.0, 'data': (3.8219, 1.0368, -0.6050), 'unit':'m2', 'Fbare': 1.34 }
        Vibrating = { 'min_size': 0.3, 'max_size': 15.0, 'data': (4.0185, 0.1118, 0.3260), 'unit':'m2', 'Fbare': 1.34 }
    
    model: Model = Model.Rotary

class ScreenCost(Equipment):

    def __init__(self, properties: ScreenProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of screen\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(area, CEPCI)        

    def bare_module(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of screen\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._props.model.value['Fbare']
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)

    def total_module(self, area: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of screen\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(area, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))