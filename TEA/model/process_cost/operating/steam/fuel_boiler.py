from dataclasses import dataclass
from references import SteamTable

@dataclass(frozen=True)
class FuelInformation:
    """
        price ($/kg) - fuel price\n
        carbon_content (-) - carbon content\n
        net_heating (kJ/kg) - net heating value
    """
    price: float
    carbon_content: float
    net_heating: float

class FuelBoiler:
    def __init__(self, water_temp: float, steam_temp: float, fuel: FuelInformation, efficiency: float):
        table = SteamTable()
        self._feed_prop = table.properties_at(water_temp)
        self._steam_prop = table.properties_at(steam_temp)
        self._fuel = fuel
        self._efficiency = efficiency
        self._dHfact = (self._steam_prop["enthalpy_vap"] - self._feed_prop["enthalpy_liq"])/self._steam_prop["latent_Heat"]

    def cost(self, duty: float):
        """
            duty (kW) - process heat duty\n
            return ($/h) - steam cost
        """
        Qfuel = duty*self._dHfact*self._efficiency
        cost = Qfuel/self._fuel.price
        return cost*3600

    def emissions(self, duty: float):
        """
            duty (kW) - process heat duty
            return (kg/h) - CO2 emissions 
        """
        Qfuel = duty*self._dHfact*self._efficiency
        emissions = Qfuel*3.67*self._fuel.carbon_content/self._fuel.net_heating
        return emissions*3600

    def quantity(self, duty: float):
        """
            duty (kW) - process heat duty
            return (kg/h) - fuel flowrate
        """
        Qfuel = duty*self._dHfact*self._efficiency
        quantity = Qfuel/self._fuel.net_heating
        return quantity*3600