from .model.process_cost.capital.capital_cost_model import CapitalCostModel

class ScenarioForm:
    def __init__(self, CEPCI: float, contingency: float= 0.18):
        self._CEPCI = CEPCI
        self._contingency = contingency
        self._capex = CapitalCostModel(CEPCI, contingency)

    @property
    def capital_cost(self) -> CapitalCostModel:
        return self._capex
    
    @property
    def opex(self):
        pass



