from dataclasses import dataclass
from enum import Enum
from .core import EquipmentProperties, EquipmentPurchased, EquipmentCostResult, EquipmentCost
from .pressure import HeatExchangerPressure

@dataclass(frozen=True)
class HeatExchangerProperties:
    """
    pressure (barg) - Operating pressure\n
    """
    class Material(Enum):
        CarbonSteel = {'DoublePipe': 1.0, 'MultiplePipe': 1.0, 'FixedTube': 1.0, 'FloatingHead': 1.0, 'UTube': 1.0, 'Bayonet': 1.0, 'KettleReboiler': 1.0, 'ScrapedWall': 1.0, 'SpiralTube': 1.0,
                       'AirCooler': 1.0, 'FlatPlate': 1.0, 'SpiralPlate': 1.0, 'TeflonTube': 1.0}
        StainlessSteel = {'DoublePipe': 2.74, 'MultiplePipe': 2.74, 'FixedTube': 2.74, 'FloatingHead': 2.74, 'UTube': 2.74, 'Bayonet': 2.74, 'KettleReboiler': 2.74, 'ScrapedWall': 2.74, 'SpiralTube': 2.74,
                          'AirCooler': 2.95, 'FlatPlate': 2.45, 'SpiralPlate': 2.45, 'TeflonTube': 1.0}
        Copper = {'DoublePipe':1.67, 'MultiplePipe':1.67, 'FixedTube': 1.67, 'FloatingHead': 1.67, 'UTube': 1.67, 'Bayonet': 1.67, 'KettleReboiler': 1.67, 'ScrapedWall': 1.67, 'SpiralTube': 1.67,
                  'AirCooler': 1.1, 'FlatPlate': 1.36, 'SpiralPlate': 1.36}
        NiAlloy = {'DoublePipe': 3.74, 'MultiplePipe': 3.74, 'FixedTube': 3.74, 'FloatingHead': 3.74, 'UTube': 3.74, 'Bayonet': 3.74, 'KettleReboiler': 3.74, 'ScrapedWall': 3.74, 'SpiralTube': 3.74,
                   'FlatPlate': 2.7, 'SpiralPlate': 2.7, 'TeflonTube': 1.0}
        Titanium = {'DoublePipe': 11.4, 'MultiplePipe': 11.4, 'FixedTube': 11.4, 'FloatingHead': 11.4, 'UTube': 11.4, 'Bayonet': 11.4, 'KettleReboiler': 11.4, 'ScrapedWall': 11.4, 'SpiralTube': 11.4,
                    'FlatPlate': 4.66, 'SpiralPlate': 4.66, 'TeflonTube': 1.0}        
        CS_Cu = {'DoublePipe': 1.36, 'MultiplePipe': 1.36, 'FixedTube': 1.36, 'FloatingHead': 1.36, 'UTube': 1.36, 'Bayonet': 1.36, 'KettleReboiler': 1.36, 'ScrapedWall': 1.36, 'SpiralTube': 1.36 }
        CS_SS = {'DoublePipe': 1.8, 'MultiplePipe': 1.8, 'FixedTube': 1.8, 'FloatingHead': 1.8, 'UTube': 1.8, 'Bayonet': 1.8, 'KettleReboiler': 1.8, 'ScrapedWall': 1.8, 'SpiralTube': 1.8,
                 'AirCooler': 1.1, 'FlatPlate': 2.2, 'SpiralPlate': 2.2, 'TeflonTube': 1.0}
        CS_NiAlloy = {'DoublePipe': 2.66, 'MultiplePipe': 2.66, 'FixedTube': 2.66, 'FloatingHead': 2.66, 'UTube': 2.66, 'Bayonet': 2.66, 'KettleReboiler': 2.66, 'ScrapedWall': 2.66, 'SpiralTube': 2.66,
                      'FlatPlate': 2.2, 'SpiralPlate': 2.2, 'TeflonTube': 1.0}
        CS_Titanium = {'DoublePipe': 4.63, 'MultiplePipe': 4.63, 'FixedTube': 4.63, 'FloatingHead': 4.63, 'UTube': 4.63, 'Bayonet': 4.63, 'KettleReboiler': 4.63, 'ScrapedWall': 4.63, 'SpiralTube': 4.63,
                       'FlatPlate': 2.2, 'SpiralPlate': 2.2, 'TeflonTube': 1.0}
        Aluminium = {'AirCooler': 1.43}

    class Model(Enum):
        DoublePipe = { 'min_size': 1.0, 'max_size': 10.0, 'data': (3.3444, 0.2745, -0.0472), 'unit': 'm2', 'B1':1.74, 'B2': 1.55 }
        MultiplePipe = { 'min_size': 10.0, 'max_size': 100.0, 'data': (2.7652, 0.7282, 0.0783), 'unit': 'm2', 'B1':1.74, 'B2': 1.55 }
        FixedTube = { 'min_size': 10.0, 'max_size': 1000.0, 'data': (4.3247, -0.3030, 0.1634), 'unit': 'm2', 'B1':1.63, 'B2': 1.66 }
        FloatingHead = { 'min_size': 10.0, 'max_size': 1000.0, 'data': (4.8306, -0.8509, 0.3187), 'unit': 'm2', 'B1':1.63, 'B2': 1.66 }
        UTube = { 'min_size': 10.0, 'max_size': 1000.0, 'data': (4.1884, -0.2503, 0.1974), 'unit': 'm2', 'B1':1.63, 'B2': 1.66 }
        Bayonet = { 'min_size': 10.0, 'max_size': 1000.0, 'data': (4.2768, -0.0495, 0.1431), 'unit': 'm2', 'B1':1.63, 'B2': 1.66 }
        KettleReboiler = { 'min_size': 10.0, 'max_size': 100.0, 'data': (4.4646, -0.5277, 0.3955), 'unit': 'm2', 'B1':1.63, 'B2': 1.66 }
        ScrapedWall = { 'min_size': 2.0, 'max_size': 20.0, 'data': (3.7803, 0.8569, 0.0349), 'unit': 'm2', 'B1':1.74, 'B2': 1.55 }
        SpiralTube = { 'min_size': 1.0, 'max_size': 100.0, 'data': (3.9912, 0.0668, 0.2430), 'unit': 'm2', 'B1':1.74, 'B2': 1.55 }
        AirCooler = { 'min_size': 10.0, 'max_size': 10000.0, 'data': (4.0336, 0.2341, 0.0497), 'unit': 'm2', 'B1':0.96, 'B2': 1.21 }
        TeflonTube = { 'min_size': 1.0, 'max_size': 10.0, 'data': (3.8062, 0.8924, -0.1671), 'unit': 'm2', 'B1':1.63, 'B2': 1.66 }
        FlatPlate = { 'min_size': 10.0, 'max_size': 1000.0, 'data': (4.6656, -0.1557, 0.1547), 'unit': 'm2', 'B1':0.96, 'B2': 1.21 }
        SpiralPlate = { 'min_size': 1.0, 'max_size': 100.0, 'data': (4.6561, -0.2947, 0.2207), 'unit': 'm2', 'B1':0.96, 'B2': 1.21 }

    material: Material = Material.CarbonSteel
    model: Model = Model.FloatingHead
    tube_only: bool= True
    pressure: float= 0.0


class HeatExchangerCost(EquipmentCost):

    def __init__(self, properties: HeatExchangerProperties) -> None:
        self._props = properties
        self._pressure = HeatExchangerPressure(properties.model.name, properties.tube_only)
        self._equipment= EquipmentPurchased(EquipmentProperties(data=properties.model.value['data'],
                                                                unit=properties.model.value['unit'],
                                                                min_size=properties.model.value['min_size'],
                                                                max_size=properties.model.value['max_size']))

    def purchased(self, area: float, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of heat exchanger\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Purchased cost of equipment
        """
        return self._equipment.cost(area, CEPCI)        

    def bare_module(self, area: float,CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of heat exchanger\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Bare module cost (Direct and indirect costs)
        """
        Fm = self._props.material.value[self._props.model.name]
        Fp = self._pressure.factor(self._props.pressure)
        B1 = self._props.model.value['B1']
        B2 = self._props.model.value['B1']
        cp0 = self._equipment.cost(area, CEPCI)
        return EquipmentCostResult(status= {'size': cp0.status['size'], 'pressure': Fp.status},
                                   CEPCI= CEPCI,
                                   value= cp0.value*(B1 + B2*Fm*Fp.value))

    def total_module(self, area: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        """
            area (m2) - Area of heat exchanger\n
            CEPCI (-) - Chemical plant cost indexes\n
            return ($) - Total module cost (Direct, indirect, fee and contingency costs)
        """
        bar_module = self.bare_module(area, CEPCI)
        return EquipmentCostResult(status= bar_module.status,
                                   CEPCI= CEPCI,
                                   value= bar_module.value*(1 + fraction))