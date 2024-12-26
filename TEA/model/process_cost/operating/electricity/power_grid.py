from dataclasses import dataclass

@dataclass(frozen=True)
class PowerGridProperties:
    """
        price ($/kWh) - Electricity price\n
        grid_emssion (kgCO2/kWh) - electricity grid emission factor\n
    """
    price: float
    grid_emissions: float

class PowerGrid:
    def __init__(self, properties: PowerGridProperties):
        self._props = properties
        
    def cost(self, energy: float):
        """
            energy (kW) - electric energy\n
            return ($/h) - steam cost
        """
        return energy*self._props.price
    
    def emissions(self, energy: float):
        """
            energy (kW) - electric energy\n
            return (kgCO2/h) - CO2 emissions 
        """
        return  energy*self._props.grid_emissions