from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

@dataclass(frozen=True)
class CompressorProperties:
    class Material(Enum):
        CarbonSteel = {'Centrifugal': 2.78, 'Axial': 3.85, 'Reciprocating': 3.37, 'Rotary': 2.41}
        StainlessSteel = {'Centrifugal': 5.77, 'Axial': 8.03, 'Reciprocating': 7.01, 'Rotary': 5.07}
        NiAlloy = {'Centrifugal': 11.49, 'Axial': 16.0, 'Reciprocating': 13.92, 'Rotary': 9.9}

    class Model(Enum):
        Centrifugal = { 'min_size': 450.0, 'max_size': 3000.0, 'data': (2.2897, 1.3604, -0.1027), 'unit':'kW' }
        Axial = { 'min_size': 450.0, 'max_size': 3000.0, 'data': (2.2897, 1.3604, -0.1027), 'unit':'kW' }
        Reciprocating = { 'min_size': 450.0, 'max_size': 3000.0, 'data': (2.2897, 1.3604, -0.1027), 'unit':'kW' }
        Rotary = { 'min_size': 18.0, 'max_size': 950.0, 'data': (5.0355, -1.8002, 0.8253), 'unit':'kW' }

    material: Material= Material.CarbonSteel
    model: Model= Model.Centrifugal

class CompressorCost(Equipment):
    def __init__(self, properties: CompressorProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of compressor\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(power, CEPCI)        

    def bare_module(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of compressor\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._props.material.value[self._props.model.name]
        cp0 = self._equipment.cost(power, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)

    def total_module(self, power: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of compressor\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(power, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))