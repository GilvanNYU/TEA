from dataclasses import dataclass

@dataclass(frozen=True)
class ElectricityInformation:
    """
        price ($/kWh) - Electricity price\n
        grid_emssion (kgCO2/kWh) - electricity grid emission factor\n
    """
    price: float
    grid_emissions: float

class ElectricBoiler:
    def __init__(self, electricity: ElectricityInformation, efficiency: float):
        self._efficiency = efficiency
        self._elect = electricity

    def cost(self, energy: float):
        """
            energy (kW) - process energy consumption\n
            return ($/h) - steam cost
        """
        return self.quantity(energy)*self._elect.price

    def emissions(self, energy: float):
        """
            energy (kW) - process energy consumption\n
            return (kgCO2/h) - CO2 emissions 
        """
        return  self.quantity(energy)*self._elect.grid_emissions

    def quantity(self, energy: float):
        """
            energy (kW) - process energy consumption\n
            return (kW) - electricity usage
        """
        return energy/self._efficiency