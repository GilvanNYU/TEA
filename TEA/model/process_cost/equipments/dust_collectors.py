from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

@dataclass(frozen=True)
class DustCollectorProperties:
    class Model(Enum):
        Baghouse = { 'min_size': 0.08, 'max_size': 350.0, 'data': (4.5007, 0.4182, 0.0813), 'unit':'m3', 'Fbare': 2.86}
        CycloneScrubbers =  { 'min_size': 0.06, 'max_size': 200.0, 'data': (3.6298, 0.5009, 0.0411), 'unit':'m3', 'Fbare': 2.86 }
        ElectrostaticPrecipitator = { 'min_size': 0.06, 'max_size':200.0, 'data': (3.6298, 0.5009, 0.0411), 'unit':'m3', 'Fbare': 2.86 }
        VenturiScrubber = { 'min_size': 0.06, 'max_size': 200.0, 'data': (3.6298, 0.5009, 0.0411), 'unit':'m3', 'Fbare': 2.86 }
    
    model: Model = Model.Baghouse


class DustCollectorCost(Equipment):
    def __init__(self, properties: DustCollectorProperties) -> None:
        self._props = properties
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of dust collectors\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(volume, CEPCI)        

    def bare_module(self, volume: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            volume (m3) - Volume of dust collectors\n
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
            volume (m3) - Volume of dust collectors\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(volume, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))