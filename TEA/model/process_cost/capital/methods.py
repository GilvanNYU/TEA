from .core.area_model import AreaModel
from .result_classes.capital_cost_result import CapitalCostResult
from .result_classes.equipment_result import EquipmentResult

def purchased_method(areas: dict[str, AreaModel], CEPCI: float) -> CapitalCostResult:
    results = CapitalCostResult()
    for area_name, area_data in areas.items():
        results.create_area(area_name)
        for unit_operation in area_data.unit_operations:
            for equipment in unit_operation.equipments:
                result = EquipmentResult(equipment.name,
                                         equipment.model.purchased(equipment.size, CEPCI))
                results.area(area_name).add_equipment(unit_operation.name, result)
    return results


def bare_module_method(areas: dict[str, AreaModel], CEPCI: float) -> CapitalCostResult:
    results = CapitalCostResult()
    for area_name, area_data in areas.items():
        results.create_area(area_name)
        for unit_operation in area_data.unit_operations:            
            for equipment in unit_operation.equipments:
                result = EquipmentResult(equipment.name,
                                         equipment.model.bare_module(equipment.size, CEPCI))
                results.area(area_name).add_equipment(unit_operation.name, result)
    return results


def total_module_method(areas: dict[str, AreaModel], CEPCI: float, contingency: float) -> CapitalCostResult:
    results = CapitalCostResult()
    for area_name, area_data in areas.items():
        results.create_area(area_name)
        for unit_operation in area_data.unit_operations:            
            for equipment in unit_operation.equipments:
                result = EquipmentResult(equipment.name,
                                         equipment.model.total_module(equipment.size, contingency, CEPCI))
                results.area(area_name).add_equipment(unit_operation.name, result)
    return results
