
class GenericMaterial:
    def __init__(self, name: str, price: float, emissions: float):
        self._name = name
        self._price = price
        self._emissions = emissions

    def cost(self, flow: float) -> float:
        return flow*self._price
    
    def emissions(self, flow: float) -> float:
        return flow*self._emissions
    
    def name(self) -> str:
        return self._name