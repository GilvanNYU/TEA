from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, EquipmentCost
from .pressure import PumpPressure

@dataclass(frozen=True)
class PumpProperties:
    """
    pressure (barg) - Operating pressure\n
    """
    class Material(Enum):
        CastIron = {'Reciprocating': 1.00, 'PositiveDisplacement': 1.00, 'Centrifugal': 1.0}
        CarbonSteel = {'Reciprocating': 1.45, 'PositiveDisplacement': 1.42, 'Centrifugal': 1.54}
        CuAlloy = {'Reciprocating': 1.29, 'PositiveDisplacement': 1.29}
        StainlessSteel = {'Reciprocating': 2.35, 'PositiveDisplacement': 2.66, 'Centrifugal': 2.31}
        NiAlloy = {'Reciprocating': 3.96, 'PositiveDisplacement': 4.75, 'Centrifugal': 4.36}
        Titanium = {'Reciprocating': 6.45, 'PositiveDisplacement': 10.68}

    class Model(Enum):
        Reciprocating = { 'min_size': 0.1, 'max_size': 200.0, 'data': (3.8696, 0.3161, 0.1220), 'unit': 'kW', 'B1':1.89, 'B2': 1.35 }
        PositiveDisplacement = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.4771, 0.1350, 0.1438), 'unit': 'kW', 'B1':1.89, 'B2': 1.35 }
        Centrifugal = { 'min_size': 1.0, 'max_size': 300.0, 'data': (3.3892, 0.0536, 0.1538), 'unit': 'kW', 'B1':1.89, 'B2': 1.35 }

    material: Material= Material.CarbonSteel
    model: Model= Model.Centrifugal
    pressure: float = 0
    
class PumpCost(EquipmentCost):
    def __init__(self, properties: PumpProperties) -> None:
        self._props = properties
        self._pressure = PumpPressure(properties.model.name)
        self._equipment: EquipmentPurchased = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                                     unit=properties.model.value['unit'],
                                                                                     min_size=properties.model.value['min_size'],
                                                                                     max_size=properties.model.value['max_size']))

    def purchased(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - power of pump\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(power, CEPCI)        

    def bare_module(self, power: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - power of pump\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        Fm = self._props.material.value[self._props.model.name]
        Fp = self._pressure.factor(self._props.pressure)
        B1 = self._props.model.value['B1']
        B2 = self._props.model.value['B1']
        cp0 = self._equipment.cost(power, CEPCI)
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*(B1 + B2*Fm*Fp.value))

    def total_module(self, power: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            power (kW) - power of pump\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(power, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))