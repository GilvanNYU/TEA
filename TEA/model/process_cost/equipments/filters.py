from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

@dataclass(frozen=True)
class FilterProperties:
    class Model(Enum):
        Bent = { 'min_size': 0.9, 'max_size': 115.0, 'data': (5.1055, 0.4999, 0.0001), 'unit':'m2', 'Fbare': 1.65 }
        Cartridge = { 'min_size': 15.0, 'max_size': 200.0, 'data': (3.2107, 0.7597, 0.0027), 'unit':'m2', 'Fbare': 1.65 }
        Disc = { 'min_size': 0.9, 'max_size': 300.0, 'data': (4.8123, 0.2858, 0.0420), 'unit':'m2', 'Fbare': 1.65 }
        Drum = { 'min_size': 0.9, 'max_size': 300.0, 'data': (4.8123, 0.2858, 0.0420), 'unit':'m2', 'Fbare': 1.65 }
        Gravity = { 'min_size': 0.5, 'max_size': 80.0, 'data': (4.2756, 0.3520, 0.0714), 'unit':'m2', 'Fbare': 1.65 }
        Leaf = { 'min_size': 0.6, 'max_size': 235.0, 'data': (3.8187, 0.6235, 0.0176), 'unit':'m2', 'Fbare': 1.65 }
        Pan = { 'min_size': 0.9, 'max_size': 300.0, 'data': (4.8123, 0.2858, 0.0420), 'unit':'m2', 'Fbare': 1.65 }
        Plate = { 'min_size': 0.5, 'max_size': 80.0, 'data': (4.2756, 0.3520, 0.0714), 'unit':'m2', 'Fbare': 1.8 }
        Frame = { 'min_size': 0.5, 'max_size': 80.0, 'data': (4.2756, 0.3520, 0.0714), 'unit':'m2', 'Fbare': 1.8 }
        Table = { 'min_size': 0.9, 'max_size': 115.0, 'data': (5.1055, 0.4999, 0.0001), 'unit':'m2', 'Fbare': 1.65 }
        Tube = { 'min_size': 0.9, 'max_size': 115.0, 'data': (5.1055, 0.4999, 0.0001), 'unit':'m2', 'Fbare': 1.65 }

    model: Model = Model.Bent

class FilterCost(Equipment):
    def __init__(self, properties: FilterProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of filter\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(area, CEPCI)        

    def bare_module(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of filter\n
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
            area (m2) - Area of filter\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(area, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))