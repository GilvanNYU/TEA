from dataclasses import dataclass
import math
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

@dataclass(frozen=True)
class TrayProperties:
    """
    num_trays (-) - number of trays\n
    """
    class Material(Enum):
        CarbonSteel = {'Sieve': 1.05, 'Valve': 1.05, 'Demisters': 1.05}
        StainlessSteel = {'Sieve': 1.89, 'Valve': 1.89, 'Demisters': 1.05}
        NiAlloy = {'Sieve': 5.6, 'Valve': 5.6, 'Demisters': 5.6}
        Fluorocarbon = {'Sieve': 1.84, 'Valve': 1.84, 'Demisters': 1.84}

    class Model(Enum):
        Sieve = { 'min_size': 0.07, 'max_size': 12.3, 'data': (2.9949, 0.4465, 0.3961), 'unit': 'm2'}
        Valve = { 'min_size': 0.7, 'max_size': 10.5, 'data': (3.3322, 0.4838, 0.3434), 'unit': 'm2'}
        Demisters = { 'min_size': 0.7, 'max_size': 10.5, 'data': (3.2353, 0.4838, 0.3434), 'unit': 'm2'}

    material: Material = Material.CarbonSteel
    model: Model = Model.Sieve
    num_trays: int = 10

class TrayCost(Equipment):
    def __init__(self, properties: TrayProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of tray\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*self._props.num_trays)       

    def bare_module(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of tray\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        Fq = 1
        if self._props.num_trays < 20:
            log10 = math.log10(self._props.num_trays)
            Fq = 0.4771 + 0.08516*log10 - 0.3473*(log10**2)
        FBM = self._props.material.value[self._props.model.name]
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fq*self._props.num_trays)

    def total_module(self, area: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - area of tray\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(area, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))