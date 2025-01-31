from enum import Enum
from dataclasses import dataclass
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, EquipmentCost

@dataclass(frozen=True)
class TowerStructure:
    max_stress: float = 944
    min_thickness: float = 0.0063
    corrosion_allowance: float = 0.00315
    weld_efficiency: float = 0.9

@dataclass(frozen=True)
class TowerProperties:
    """
    pressure (barg) - Operating pressure\n
    diameter (m) - diameter of vessel\n
    """
    class Material(Enum):
        CarbonSteel = 1.0
        StainlessSteelClad = 1.75
        StainlessSteel = 3.12
        NiAlloyClad = 3.63
        NiAlloy = 7.09
        TitaniumClad = 4.71
        Titanium = 9.43

    class Model(Enum):
        Tower = { 'min_size': 0.3, 'max_size': 520.0, 'data': (3.4974, 0.4485, 0.1074), 'unit': 'm3', 'B1': 2.25, 'B2': 1.82 }

    material: Material= Material.CarbonSteel
    model: Model= Model.Tower
    structure: TowerStructure= TowerStructure()
    pressure: float = 0
    diameter: float = 1

    def pressure_factor(self):
        t = (self.pressure + 1)*self.diameter/(2*self.structure.max_stress*self.structure.weld_efficiency - 1.2*self.pressure) + self.structure.corrosion_allowance
        if self.pressure < -0.5:
            return 1.25
        else:
            Fp = t/self.structure.min_thickness
            if Fp < 1.0:
                return 1.0
            return Fp

class TowerCost(EquipmentCost):
    def __init__(self, properties: TowerProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of tower\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of tower\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        Fp = self._props.pressure_factor()
        Fm = self._props.material.value
        B1 = self._props.model.value['B1']
        B2 = self._props.model.value['B1']
        FBM = B1 + B2*Fm*Fp
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(status= cp0.status,
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM)

    def total_module(self, volume: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of tower\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(volume, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))