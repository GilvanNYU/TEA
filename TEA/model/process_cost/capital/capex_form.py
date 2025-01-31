from .equipments.core.equipment_result import EquipmentCostResult
from .unit_operation_form import UnitOperationForm

class CapexForm:
    def __init__(self, CEPCI: float, fee: float= 0.18):
        self._CEPCI = CEPCI
        self._fee = fee
        self._units: dict[str, UnitOperationForm] = {}

    def new_unit(self, name: str) -> None:
        self._units[name] = UnitOperationForm(name)

    def units(self) -> list[UnitOperationForm]:
        return list(self._units.values())

    def unit(self, name: str) -> UnitOperationForm:
        return self._units[name]
    
    def purchased(self) -> dict[str, dict[str, list[EquipmentCostResult]]]:
        cost = {}
        for unit_name, unit in self._units.items():
            cost[unit_name] = {}
            for operations in unit.unit_operations():
                operation_name, operation_equips = operations
                cost[unit_name][operation_name] = []
                for form in operation_equips:
                    cost[unit_name][operation_name].append(form.model.purchased(form.size,
                                                                                self._CEPCI))
        return cost

    def bare_module(self) -> dict[str, dict[str, list[EquipmentCostResult]]]:
        cost = {}
        for unit_name, unit in self._units.items():
            cost[unit_name] = {}
            for operations in unit.unit_operations():
                operation_name, operation_equips = operations
                cost[unit_name][operation_name] = []
                for form in operation_equips:
                    cost[unit_name][operation_name].append(form.model.bare_module(form.size,
                                                                                  self._CEPCI))
        return cost
    
       

    def total_module(self) -> dict[str, dict[str, list[EquipmentCostResult]]]:
        cost = {}
        for unit_name, unit in self._units.items():
            cost[unit_name] = {}
            for operations in unit.unit_operations():
                operation_name, operation_equips = operations
                cost[unit_name][operation_name] = []
                for form in operation_equips:
                    cost[unit_name][operation_name].append(form.model.bare_module(form.size,
                                                                                  self._fee,
                                                                                  self._CEPCI))
        return cost