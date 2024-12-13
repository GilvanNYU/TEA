from dataclasses import dataclass

@dataclass(frozen=True)
class ElectricityInformation:
    """
        price ($/kWh) - Electricity price\n
        grid_emssion (kgCO2/kWh) - electricity grid emission factor\n
        net_heating (kJ/kg) - net heating value
    """
    price: float
    grid_emissions: float
    net_heating: float

class ElectricBoiler:
    def __init__(self, electricity: ElectricityInformation, efficiency: float):
        self._efficiency = efficiency
        self._elect = electricity

    def cost(self, duty: float):
        """
            duty (kW) - process heat duty\n
            return ($/h) - steam cost
        """
        return duty*self._elect.price/self._efficiency

    def emissions(self, duty: float):
        """
            duty (kW) - process heat duty
            return (kg/h) - CO2 emissions 
        """
        return duty*self._elect.grid_emissions/self._efficiency

    def quantity(self, duty: float):
        """
            duty (kW) - process heat duty
            return (kg/h) - fuel flowrate
        """
        return duty/self._efficiency