from enum import Enum
from .pressure import FanPressure
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, Equipment

class FanProperties:
    """
    rise pressure (kPa) - Rise pressure
    """
    class Material(Enum):
        CarbonSteel = {'CentrifugalRadial': 2.74, 'BackwardCurve': 2.74, 'AxialVane': 2.74, 'AxialTube': 2.74}
        Fiberglass = {'CentrifugalRadial': 5.03, 'BackwardCurve': 5.03, 'AxialVane': 5.03, 'AxialTube': 5.03}
        NiAlloy = {'CentrifugalRadial': 5.78, 'BackwardCurve': 5.78, 'AxialVane': 5.78, 'AxialTube': 5.78}
        StainlessSteel = {'CentrifugalRadial': 11.52, 'BackwardCurve': 11.52, 'AxialVane': 11.52, 'AxialTube': 11.52}

    class Model(Enum):
        CentrifugalRadial = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.5391, -0.3533, 0.4477), 'unit':'m3/s' }
        BackwardCurve = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.3471, -0.0734, 0.3090), 'unit':'m3/s' }
        AxialVane = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.1761, -0.1373, 0.3414), 'unit':'m3/s' }
        AxialTube = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.0414, -0.3375, 0.4722), 'unit':'m3/s' }

    material: Material = Material.CarbonSteel
    model: Model = Model.CentrifugalRadial
    rise_pressure: float = 0.0

class FanCost(Equipment):
    def __init__(self, properties: FanProperties) -> None:
        self._props = properties
        self._pressure: FanPressure = FanPressure(properties.model.name)
        self._equipment = EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                 unit=properties.model.value['unit'],
                                                                 min_size=properties.model.value['min_size'],
                                                                 max_size=properties.model.value['max_size']))

    def purchased(self, flowrate: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            flowrate (m3/s) - Gas flowrate of fans\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(flowrate, CEPCI)        

    def bare_module(self, flowrate: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            flowrate (m3/s) - Gas flowrate of fans\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        FBM = self._props.material.value[self._props.model.name]
        Fp = self._pressure.factor(self._props.rise_pressure)
        cp0 = self._equipment.cost(flowrate, CEPCI)
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*FBM*Fp.value)

    def total_module(self, flowrate: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            flowrate (m3/s) - Gas flowrate of fans\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(flowrate, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))