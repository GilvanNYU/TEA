from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment
from .pressure import VaporizerPressure

@dataclass(frozen=True)
class VaporizerProperties:
    """
    pressure (barg) - Operating pressure\n    
    """
    class Material(Enum):
        CarbonSteel = {'InternalCoils': 3.04, 'JacketedVessels': 2.73}
        Copper = {'InternalCoils': 3.83, 'JacketedVessels': 3.45}
        GlassSS = {'InternalCoils': 5.19, 'JacketedVessels': 4.67}
        GlassNi = {'InternalCoils': 5.49, 'JacketedVessels': 4.95}
        StainlessSteel = {'InternalCoils': 5.19, 'JacketedVessels': 4.81}
        StainlessSteelClad = {'InternalCoils': 4.16, 'JacketedVessels': 3.83}
        NiAlloy = {'InternalCoils': 10.14, 'JacketedVessels': 9.15}
        NiAlloyClad = {'InternalCoils': 6.64, 'JacketedVessels': 6.00}
        Titanium = {'InternalCoils': 15.23, 'JacketedVessels': 13.78}
        TitaniumClad = {'InternalCoils': 10.66, 'JacketedVessels': 9.69}

    class Model(Enum):
        InternalCoils = { 'min_size': 1.0, 'max_size': 100.0, 'data': (4.0000, 0.4321, 0.1700), 'unit':'m3'}
        JacketedVessels = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.8751, 0.3328, 0.1901), 'unit':'m3'}

    material: Material = Material.CarbonSteel
    model: Model = Model.JacketedVessels
    pressure: float = 0.0

class VaporizerCost(Equipment):
    def __init__(self, properties: VaporizerProperties) -> None:
        self._props = properties
        self._pressure = VaporizerPressure()           
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Gas volume of vaporizer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of vaporizer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._props.material.value[self._props.model.name]
        Fp = self._pressure.factor(self._props.pressure)
        cp0 = self._equipment.cost(volume, CEPCI)
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp.value)

    def total_module(self, volume: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of vaporizer\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(volume, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))