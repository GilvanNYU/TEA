from dataclasses import dataclass
from ..core.steam_table import SteamTable

@dataclass(frozen=True)
class ElectricityInformation:
    """
        price ($/kWh) - Electricity price\n
        grid_emssion (kgCO2/kWh) - electricity grid emission factor\n
    """
    price: float
    grid_emissions: float

class ElectricBoiler:
    def __init__(self, water_temp: float, steam_temp: float, electricity: ElectricityInformation, efficiency: float):
        table = SteamTable()
        self._feed_prop = table.properties_at(water_temp)
        self._steam_prop = table.properties_at(steam_temp)
        self._dHfact = (self._steam_prop["enthalpy_vap"] - self._feed_prop["enthalpy_liq"])/self._steam_prop["latent_Heat"]
        self._efficiency = efficiency
        self._elect = electricity

    def cost(self, duty: float):
        """
            duty (kW) - process heat duty\n
            return ($/h) - steam cost
        """
        return self.quantity(duty)*self._elect.price

    def emissions(self, duty: float):
        """
            duty (kW) - process heat duty\n
            return (kgCO2/h) - CO2 emissions 
        """
        return  self.quantity(duty)*self._elect.grid_emissions

    def quantity(self, duty: float):
        """
            duty (kW) - process heat duty\n
            return (kW) - electricity usage
        """
        Qelec = duty*self._dHfact/self._efficiency
        return Qelec