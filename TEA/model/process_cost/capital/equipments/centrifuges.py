from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

@dataclass(frozen=True)
class CentrifugeProperties:
    class Model(Enum):
        Apron = {'min_size':  1.0, 'max_size': 15.0, 'data': (3.9255, 0.5039, 0.1506), 'unit':'m2', 'Fbare': 1.20}
        Belt = {'min_size': 0.5, 'max_size': 325.0, 'data': (4.0637, 0.2584, 0.1550), 'unit':'m2', 'Fbare': 1.25}
        Pneumatic = {'min_size': 0.75, 'max_size': 65.0, 'data': (4.6616, 0.3205, 0.0638), 'unit':'m2', 'Fbare': 1.25}
        Screw = {'min_size': 0.5, 'max_size': 30.0, 'data': (3.6062, 0.2659, 0.1982), 'unit':'m2', 'Fbare': 1.10}
    
    model: Model = Model.Apron

class CentrifugeCost(Equipment):

    def __init__(self, properties: CentrifugeProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of centrifuge\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(area, CEPCI)        

    def bare_module(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of centrifuge\n
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
            area (m2) - Area of centrifuge\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(area, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))
    