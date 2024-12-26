from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment
from .pressure import TankPressure

@dataclass(frozen=True)
class TankProperties:
    """
    pressure (barg) - Operating pressure\n
    """
    class Material(Enum):
        CarbonSteel = {'APIFixedRoof': 1.0, 'APIFloatingRoof': 1.0}
        StainlessSteelClad = {'APIFixedRoof': 1.75, 'APIFloatingRoof': 1.75}
        StainlessSteel = {'APIFixedRoof': 3.12, 'APIFloatingRoof': 3.12}
        NiAlloyClad = {'APIFixedRoof': 3.63, 'APIFloatingRoof': 3.63}
        NiAlloy = {'APIFixedRoof': 7.09, 'APIFloatingRoof': 7.09}
        TitaniumClad = {'APIFixedRoof': 4.71, 'APIFloatingRoof': 4.71}
        Titanium = {'APIFixedRoof': 9.43, 'APIFloatingRoof': 9.73}

    class Model(Enum):
        APIFixedRoof = { 'min_size': 90.0, 'max_size': 30000.0, 'data': (4.8509, -0.3973, 0.1445), 'unit': 'm3', 'B1': 2.25, 'B2': 1.82 }
        APIFloatingRoof = { 'min_size': 1000.0, 'max_size': 40000.0, 'data': (5.9567, -0.7585, 0.1749), 'unit': 'm3', 'B1': 2.25, 'B2': 1.82 }

    material: Material = Material.CarbonSteel
    model: Model= Model.APIFixedRoof
    pressure: float = 0.0

class TankCost(Equipment):
    def __init__(self, properties: TankProperties) -> None:
        self._props = properties
        self._pressure = TankPressure()
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of tank\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of tank\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        Fm = self._props.material.value[self._props.model.name]
        Fp = self._pressure.factor(self._props.pressure)
        B1 = self._props.model.value['B1']
        B2 = self._props.model.value['B1']
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*(B1 + B2*Fm*Fp.value))

    def total_module(self, volume: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of tank\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(volume, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))