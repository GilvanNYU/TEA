from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, EquipmentCost

@dataclass(frozen=True)
class DryerProperties:
    class Model(Enum):
        Drum = { 'min_size': 0.5, 'max_size': 50.0, 'data': (4.5472, 0.2731, 0.1340), 'unit':'m2', 'Fbare': 1.60}
        Rotary =  { 'min_size': 5.0, 'max_size': 100.0, 'data': (3.5645, 1.1118, -0.0777), 'unit':'m2', 'Fbare': 1.25 }
        GasFired = { 'min_size': 5.0, 'max_size': 100.0, 'data': (3.5645, 1.1118, -0.0777), 'unit':'m2', 'Fbare': 1.25 }
        Tray = { 'min_size': 1.8, 'max_size': 20.0, 'data': (3.6951, 0.5442, -0.1248), 'unit':'m2', 'Fbare': 1.25 }
    
    model: Model = Model.Drum

class DryerCost(EquipmentCost):
    def __init__(self, properties: DryerProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of dryers\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(area, CEPCI)        

    def bare_module(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of dryers\n
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
            area (m2) - Area of dryers\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(area, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))