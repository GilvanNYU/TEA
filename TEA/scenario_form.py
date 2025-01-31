from .model.process_cost.capital.capex_form import CapexForm

class ScenarioForm:
    def __init__(self, CEPCI: float, contingency: float= 0.18):
        self._CEPCI = CEPCI
        self._contingency = contingency
        self._capex = CapexForm(CEPCI, contingency)

    @property
    def capex(self) -> CapexForm:
        return self._capex
    
    @property
    def opex(self):
        pass



