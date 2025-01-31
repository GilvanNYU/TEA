from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, EquipmentCost

@dataclass(frozen=True)
class MixerProperties:
    class Model(Enum):
        Impeller = { 'min_size': 5.0, 'max_size': 150.0, 'data': (3.8511, 0.7009, -0.0003), 'unit':'kW', 'Fbare': 1.38 }
        Propeller = { 'min_size': 5.0, 'max_size': 500.0, 'data': (4.3207, 0.0359, 0.1346), 'unit':'kW', 'Fbare': 1.38 }
        Turbine = { 'min_size': 5.0, 'max_size': 150.0, 'data': (3.4092, 0.4896, 0.0030), 'unit':'kW', 'Fbare': 1.38 }

    model : Model

class MixerCost(EquipmentCost):
    def __init__(self, properties: MixerProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of mixer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(power, CEPCI)        

    def bare_module(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of mixer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM= self._props.model.value['Fbare']
        cp0 = self._equipment.cost(power, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)

    def total_module(self, power: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of mixer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(power, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))