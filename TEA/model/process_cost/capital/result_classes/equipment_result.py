from ..equipments.core.equipment_cost_result import EquipmentCostResult

class EquipmentResult:
    def __init__(self, name: str, equipments: EquipmentCostResult):
        self._name = name
        self._equips = equipments
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def cost_result(self) -> EquipmentCostResult:
        return self._equips