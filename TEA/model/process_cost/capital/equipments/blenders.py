from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, EquipmentCost

@dataclass(frozen=True)
class BlenderProperties:
    class Model(Enum):
        Kneader = { 'min_size': 0.14, 'max_size': 3.0, 'data': (5.0141, 0.5867, 0.3224), 'unit':'m3', 'Fbare': 1.12}
        Ribbon =  { 'min_size': 0.7, 'max_size': 11.0, 'data': (4.1366, 0.5072, 0.0070), 'unit':'m3', 'Fbare': 1.12 }
        Rotary = { 'min_size': 0.7, 'max_size': 11.0, 'data': (4.1366, 0.5072, 0.0070), 'unit':'m3', 'Fbare': 1.12 }

    model: Model = Model.Kneader

class BlenderCost(EquipmentCost):
    def __init__(self, properties: BlenderProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of blender\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of blender\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._props.model.value['Fbare']
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)

    def total_module(self, volume: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of blender\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(volume, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))