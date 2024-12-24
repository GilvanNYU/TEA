from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

@dataclass(frozen=True)
class ReactorProperties:
    class Model(Enum):
        Autoclave = { 'min_size': 1.0, 'max_size': 15.0, 'data': (4.5587, 0.2986, 0.0020), 'unit':'m3', 'Fbare': 4.0 }
        Fermenter = { 'min_size': 0.1, 'max_size': 35.0, 'data': (4.1052, 0.5320, -0.0005), 'unit':'m3', 'Fbare': 4.0 }
        Inoculum_Tank = { 'min_size': 0.07, 'max_size': 1.0, 'data': (3.7957, 0.4593, 0.0160), 'unit':'m3', 'Fbare': 4.0 }
        JacketedAgitated = { 'min_size': 0.1, 'max_size': 35.0, 'data': (4.1052, 0.5320, -0.0005), 'unit':'m3', 'Fbare': 4.0 }
        JacketedNonagitated = { 'min_size': 5.0, 'max_size': 45.0, 'data': (3.3496, 0.7235, 0.0025), 'unit':'m3', 'Fbare': 4.0 }
        Mixer = { 'min_size': 0.4, 'max_size': 60.0, 'data': (4.7116, 0.4479, 0.0004), 'unit':'m3', 'Fbare': 4.0 }
        Settler = { 'min_size': 0.4, 'max_size': 60.0, 'data': (4.7116, 0.4479, 0.0004), 'unit':'m3', 'Fbare': 4.0 }
    
    model: Model = Model.Autoclave

class ReactorCost(Equipment):

    def __init__(self, properties: ReactorProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of reactor\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of reactor\n
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
            volume (m3) - Volume of reactor\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(volume, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))