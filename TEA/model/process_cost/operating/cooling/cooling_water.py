from dataclasses import dataclass
from ..core import SteamTable


@dataclass(frozen=True)
class CoolingTowerProperties:
    """
        water_price ($/kg) - water price\n
        electricity_price ($/kWh) - electricity price\n
        grid_emissions (kgCO2/kWh) - electricity grid emission factor\n
        pressure_drop (kPag) - pressure drop\n
        pump_efficiency (-) - pump efficincy\n
        fan_specific_energy (kW/(m3/hr)) - specific electricity consumption of fans\n
        blowdown (-) - blowdown fraction\n
    """
    water_price: float
    electricity_price: float
    grid_emissions: float
    pressure_drop: float = 266.7 # kPa
    pump_efficiency: float = 0.75
    fan_specific_energy: float= 0.066385246 # kW/(m3/hr)
    blowdown: float = 0.013   


class CoolingWater:
    def __init__(self, inlet_temp: float, outlet_temp: float, properties: CoolingTowerProperties):
        """
            inlet_temp (°C) - inlet temperature\n
            outlet_temp (°C) - outlet temperature\n
        """
        table = SteamTable()
        self._inlet_prop = table.properties_at(inlet_temp)
        self._outlet_prop = table.properties_at(outlet_temp)
        self._average_prop = table.properties_at((inlet_temp + outlet_temp)/2)
        self._dH = self._outlet_prop['enthalpy_liq'] - self._inlet_prop['enthalpy_liq']
        self._props = properties

    def cost(self, duty: float):
        """
            duty (kW) - process heat duty\n
            return ($/h) - cooling water cost
        """
        water = self.makeup(duty)*self._props.water_price 
        electricity = self.electric_energy(duty)*self._props.electricity_price
        
        return water + electricity

    def emissions(self, duty: float):
        """
            duty (kW) - process heat duty
            return (kgCO2/h) - CO2 emissions 
        """
        return self.electric_energy(duty)*self._props.grid_emissions

    def electric_energy(self, duty: float) -> float:
        """
            duty (kW) - process heat duty
            return (kW) - eletric energy
        """
        fans = (self.water(duty)/self._inlet_prop['density_liq'])*self._props.fan_specific_energy
        pump = (self.water(duty)/self._inlet_prop['density_liq']/3600)*self._props.pressure_drop/self._props.pump_efficiency
        return fans + pump

    def makeup(self, duty: float) -> float:
        """
            duty (kW) - process heat duty
            return (kg/h) - makeup flowrate
        """
        return self.water_loss(duty) + self.water(duty)*self._props.blowdown
    
    def water_loss(self, duty: float) -> float:
        """
            duty (kW) - process heat duty
            return (kg/h) - amount of water evaporated
        """
        return duty/self._average_prop['latent_Heat']*3600

    def water(self, duty: float) -> float:
        """
            duty (kW) - process heat duty
            return (kg/h) - cooling water flowrate
        """
        return duty/self._dH*3600