from .equipment_data import EquipmentData
from .equipment_collection import EquipmentCollection


class UnitOperationModel:
    def __init__(self, name: str):
        self._name = name
        self._equips = EquipmentCollection()

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def equipments(self) -> list[EquipmentData]:
        return self._equips.equipments
    
    def add(self, equipment: EquipmentData) -> None:
        self._equips.add(equipment)
    
    def equipment(self, name: str) -> EquipmentData:
        return self._equips[name]