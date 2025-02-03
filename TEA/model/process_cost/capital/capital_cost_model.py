from .core.area_model import AreaModel
from .result_classes.capital_cost_result import CapitalCostResult
from .methods import purchased_method, bare_module_method, total_module_method


class CapitalCostModel:
    def __init__(self, CEPCI: float, contingency: float= 0.18):
        self._CEPCI = CEPCI
        self._contingency = contingency
        self._areas: dict[str, AreaModel] = {}

    @property
    def areas(self) -> list[AreaModel]:
        return list(self._areas.values())
    
    def create_area(self, name: str) -> None:
        self._areas[name] = AreaModel(name)

    def area(self, name: str) -> AreaModel:
        return self._areas[name]
    
    def purchased(self) -> CapitalCostResult:
        return purchased_method(self._areas, self._CEPCI)

    def bare_module(self) -> CapitalCostResult:
        return bare_module_method(self._areas, self._CEPCI)

    def total_module(self) -> CapitalCostResult:
        return total_module_method(self._areas, self._CEPCI, self._contingency)
