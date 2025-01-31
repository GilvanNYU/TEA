from .unit_operation_form import UnitOperationForm
from .equipments.core.equipment_result import EquipmentCostResult


def purchased(units: dict[str, UnitOperationForm], CEPCI: float) -> dict[str, dict[str, list[EquipmentCostResult]]]:
    cost = {}
    for unit_name, unit in units.items():
        cost[unit_name] = {}
        for operations in unit.unit_operations():
            operation_name, operation_equips = operations
            cost[unit_name][operation_name] = []
            for form in operation_equips:
                cost[unit_name][operation_name].append(form.model.purchased(form.size,
                                                                            CEPCI))
    return cost

def bare_module(units: dict[str, UnitOperationForm], CEPCI: float) -> dict[str, dict[str, list[EquipmentCostResult]]]:
    cost = {}
    for unit_name, unit in units.items():
        cost[unit_name] = {}
        for operations in unit.unit_operations():
            operation_name, operation_equips = operations
            cost[unit_name][operation_name] = []
            for form in operation_equips:
                cost[unit_name][operation_name].append(form.model.bare_module(form.size,
                                                                              CEPCI))
    return cost

def total_module(units: dict[str, UnitOperationForm], CEPCI: float, contingency: float) -> dict[str, dict[str, list[EquipmentCostResult]]]:
    cost = {}
    for unit_name, unit in units.items():
        cost[unit_name] = {}
        for operations in unit.unit_operations():
            operation_name, operation_equips = operations
            cost[unit_name][operation_name] = []
            for form in operation_equips:
                cost[unit_name][operation_name].append(form.model.bare_module(form.size,
                                                                              contingency,
                                                                              CEPCI))
    return cost