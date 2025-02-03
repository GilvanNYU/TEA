from .equipment_result import EquipmentResult

class UnitOperationResult:
    def __init__(self, name: str):
        self._name = name
        self._equips: dict[str, EquipmentResult] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def equipments(self) -> list[EquipmentResult]:
        return list(self._equips.values())
    
    def equipment(self, name: str) -> EquipmentResult:
        return self._equips[name]   

    def add(self, equipment: EquipmentResult) -> None:
        self._equips[equipment.name] = equipment