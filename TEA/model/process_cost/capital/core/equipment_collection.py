from .equipment_data import EquipmentData


class EquipmentCollection:
    def __init__(self):
        self._equips: dict[str, EquipmentData] = {}
    
    @property
    def equipments(self) -> list[EquipmentData]:
        return list(self._equips.values())
    
    def add(self, equipment: EquipmentData) -> None:
        self._equips[equipment.name] = equipment

    def __getitem__(self, name: str) -> list[EquipmentData]:
        return self._equips[name]