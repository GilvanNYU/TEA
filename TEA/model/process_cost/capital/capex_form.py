from .equipments.core.equipment_result import EquipmentCostResult
from .unit_operation_form import UnitOperationForm
from .utils import purchased, bare_module, total_module

class CapexForm:
    def __init__(self, CEPCI: float, contingency: float= 0.18):
        self._CEPCI = CEPCI
        self._contingency = contingency
        self._units: dict[str, UnitOperationForm] = {}

    def new_unit(self, name: str) -> None:
        self._units[name] = UnitOperationForm(name)

    def units(self) -> list[UnitOperationForm]:
        return list(self._units.values())

    def unit(self, name: str) -> UnitOperationForm:
        return self._units[name]
    
    def purchased(self) -> dict[str, dict[str, list[EquipmentCostResult]]]:
        return purchased(self._units, self._CEPCI)


    def bare_module(self) -> dict[str, dict[str, list[EquipmentCostResult]]]:
        return bare_module(self._units, self._CEPCI)

       
    def total_module(self) -> dict[str, dict[str, list[EquipmentCostResult]]]:
        return total_module(self._units, self._CEPCI, self._contingency)
