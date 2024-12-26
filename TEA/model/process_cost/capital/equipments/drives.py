from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

@dataclass(frozen=True)
class DriveProperties:
    class Model(Enum):
        GasTurbine = { 'min_size': 7500.0, 'max_size': 23000.0, 'data': (-21.7702, 13.2175, -1.5279), 'unit':'kW', 'Fbare': 3.51 }
        InternalCombustion = { 'min_size': 10.0, 'max_size': 10000.0, 'data': (2.7635, 0.8574, -0.0098), 'unit':'kW', 'Fbare': 2.02 }
        SteamTurbine = { 'min_size': 70.0, 'max_size': 7500.0, 'data': (2.6259, 1.4398, -0.1776), 'unit':'kW', 'Fbare': 3.54 }
        ElectricExplosionProof = { 'min_size': 75.0, 'max_size': 2600.0, 'data': (2.4604, 1.4191, -0.1798), 'unit':'kW', 'Fbare': 1.50 }
        ElectricTotallyEnclosed = { 'min_size': 75.0, 'max_size': 2600.0, 'data': (1.9560, 1.7142, -0.2282), 'unit':'kW', 'Fbare': 1.5 }
        ElectricDripProof = { 'min_size': 75.0, 'max_size': 2600.0, 'data': (2.9508, 1.0688, -0.1315), 'unit':'kW', 'Fbare': 1.5 }

    model: Model = Model.SteamTurbine
    
class DriveCost(Equipment):
    def __init__(self, properties: DriveProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of drive\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(power, CEPCI)        

    def bare_module(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of drive\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM =  self._props.model.value['Fbare']
        cp0 = self._equipment.cost(power, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)

    def total_module(self, power: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - Power of drive\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(power, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))