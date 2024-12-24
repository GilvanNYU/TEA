from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

@dataclass(frozen=True)
class ConveyorProperties:
    class Model(Enum):
        AutoBatch = {'min_size': 0.5, 'max_size': 1.7, 'data': (4.7681, 0.9740, 0.0240), 'unit':'m', 'Fbare': 1.20}
        Centrifugal = {'min_size': 0.5, 'max_size': 1.0, 'data': ( 4.3657,  0.8764,  -0.0049), 'unit':'m', 'Fbare': 1.25}
        OscillatingScreen = {'min_size': 0.5, 'max_size': 1.1, 'data': (4.8600,  0.3340,  0.1063), 'unit':'m', 'Fbare': 1.25}
        SolidBowl = {'min_size': 0.3, 'max_size': 2, 'data': (4.9697, 1.1689, 0.0038), 'unit':'m', 'Fbare': 1.10}
    
    model: Model = Model.AutoBatch

class ConveyorCost(Equipment):
    def __init__(self, properties: ConveyorProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, diameter: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            diameter (m) - Diameter of conveyors\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(diameter, CEPCI)        

    def bare_module(self, diameter: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            diameter (m) - Diameter of conveyors\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._props.model.value['Fbare']
        cp0 = self._equipment.cost(diameter, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)
    
    def total_module(self, diameter: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            diameter (m) - Diameter of conveyors\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(diameter, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))