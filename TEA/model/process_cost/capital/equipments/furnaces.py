from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, EquipmentCost
from .pressure import FurnacePressure

@dataclass(frozen=True)
class FurnanceProperties:
    """
        pressure (barg) - Operating pressure\n
        deltaTemp (°C) - Amount of superheat
    """
    class Material(Enum):
        CarbonSteel = {'ReformerFurnace': 2.14, 'PyrolysisFurnace': 2.14, 'NonreactiveFiredHeater': 2.19}
        StainlessSteel = {'ReformerFurnace': 2.54, 'PyrolysisFurnace': 2.54, 'NonreactiveFiredHeater': 2.19}
        AlloySteel = {'ReformerFurnace': 2.82, 'PyrolysisFurnace': 2.82, 'NonreactiveFiredHeater': 2.19}

    class Model(Enum):
        ReformerFurnace = { 'min_size': 3000.0, 'max_size': 100000.0, 'data': (3.0680, 0.6597, 0.0194), 'unit':'kW' }
        PyrolysisFurnace = { 'min_size': 3000.0, 'max_size': 100000.0, 'data': (2.3859, 0.9721, -0.0206), 'unit':'kW' }
        NonreactiveFiredHeater = { 'min_size': 1000.0, 'max_size': 100000.0, 'data': (7.3488, -1.1666, 0.2028), 'unit':'kW' }
    
    material: Material = Material.CarbonSteel
    model: Model = Model.ReformerFurnace
    pressure: float = 0
    superheat: float = 0

class FurnanceCost(EquipmentCost):
    def __init__(self, properties: FurnanceProperties) -> None:
        self._props = properties
        self._pressure: FurnacePressure = FurnacePressure(properties.model.name)     
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, duty: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of furnace\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(duty, CEPCI)        

    def bare_module(self, duty: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of furnace\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._props.material.value[self._props.model.name]
        Ft = 1 + 0.00184*self._props.superheat - 0.00000335*(self._props.superheat**2)
        Fp = self._pressure.factor(self._props.pressure)
        cp0 = self._equipment.cost(duty, CEPCI)
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp.value*Ft)

    def total_module(self, duty: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of furnace\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(duty, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))