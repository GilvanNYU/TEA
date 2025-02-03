from .unit_operation_result import UnitOperationResult, EquipmentResult

class AreaResult:
    def __init__(self, name: str):
        self._name = name
        self._units: dict[str, UnitOperationResult] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def unit_operations(self) -> list[UnitOperationResult]:
        return list(self._units.values())
    
    def unit_operation(self, name: str) -> UnitOperationResult:
        return self._units[name]   

    def add_equipment(self, unit_name: str,  equipment: EquipmentResult) -> None:
        if unit_name not in self._units.keys():
            self._units[unit_name] = UnitOperationResult(unit_name)

        self._units[unit_name].add(equipment)