from dataclasses import dataclass
from ..core import SteamTable

@dataclass(frozen=True)
class CoolingWaterPumpSystem:
    pressure_drop: float = 266.7 # kPa
    efficiency: float = 0.75

@dataclass(frozen=True)
class CoolingWaterFanSystem:
    specific_energy: float

@dataclass(frozen=True)
class CoolingWaterMakeup:
    windage_losses: float
    max_salt: float

@dataclass(frozen=True)
class CoolingWaterProperties:
    """
        water_price ($/kg) - water price\n
        windage_losses (-) - windage losses from mechanical draft towers (0.001 - 0.003)\n
        max_salt - the maximum allowable salt concentration factor (default: 5)\n
        electricity_price ($/kWh) - Electricity price\n
        electricity_emissions (kgCO2/kWh) - electricity grid emission factor\n
    """
    fan: CoolingWaterFanSystem
    pump: CoolingWaterPumpSystem
    makeup: CoolingWaterMakeup
    water_price: float
    chemical_price: float
    electricity_price: float
    electricity_emissions: float


class CoolingWater:
    def __init__(self, inlet_temp: float, outlet_temp: float, properties: CoolingWaterProperties):
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
            return ($/h) - steam cost
        """
        cw = self.quantity(duty)
        evap = duty/self._average_prop['latent_Heat']*3600
        windage = self._props.makeup.windage_losses*cw
        blowdown = evap/(self._props.makeup.max_salt - 1) - windage
        mkup = evap + windage + blowdown

        pump = (cw/3600)/self._inlet_prop['density_liq']/self._props.pump.efficiency*self._props.pump.pressure_drop 
        fan = cw*self._props.fan.specific_energy

        return mkup*self._props.water_price + (pump + fan)*self._props.electricity_price

    def emissions(self, duty: float):
        """
            duty (kW) - process heat duty
            return (kgCO2/h) - CO2 emissions 
        """
        cw = self.quantity(duty)
        pump = (cw/3600)/self._inlet_prop['density_liq']/self._props.pump.efficiency*self._props.pump.pressure_drop 
        fan = cw*self._props.fan.specific_energy
        return (pump + fan)*self._props.electricity_emissions

    def quantity(self, duty: float):
        """
            duty (kW) - process heat duty
            return (kg/h) - cooling water flowrate
        """
        return duty/self._dH*3600