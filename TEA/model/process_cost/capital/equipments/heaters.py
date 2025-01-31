from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, EquipmentCost
from .pressure import HeaterPressure

@dataclass(frozen=True)
class HeaterProperties:
    """
    pressure (barg) - Operating pressure\n
    superheat (°C) - Amount of superheat
    """
    class Model(Enum):
        Diphenyl = { 'min_size': 650.0, 'max_size': 10750.0, 'data': (2.2628, 0.8581, 0.0003), 'unit': 'kW', 'Fbare': 2.19}
        MoltenSalt = { 'min_size': 650.0, 'max_size': 10750.0, 'data': (1.1979, 1.4782, -0.0958), 'unit': 'kW', 'Fbare': 2.19}
        HotWater = { 'min_size': 650.0, 'max_size': 10750.0, 'data': (2.0829, 0.9074, -0.0243), 'unit': 'kW', 'Fbare': 2.19}
        SteamBoiler = { 'min_size': 1200.0, 'max_size': 9400.0, 'data': (6.9617, -1.4800, 0.3161), 'unit': 'kW', 'Fbare': 2.19}

    model: Model = Model.Diphenyl
    pressure: float = 0
    superheat: float = 0

class HeaterCost(EquipmentCost):
    def __init__(self, properties: HeaterProperties) -> None:       
        self._props = properties
        self._pressure = HeaterPressure(properties.model.name)
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, duty: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of heater\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(duty, CEPCI)        

    def bare_module(self, duty: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of heater\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._props.model.value['Fbare']
        Ft = 1 + 0.00184*self._props.superheat - 0.00000335*(self._props.superheat**2)
        Fp = self._pressure.factor(self._props.pressure)
        cp0 = self._equipment.cost(duty, CEPCI)
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp.value*Ft)

    def total_module(self, duty: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            duty (kW) - Duty of heater\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(duty, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))