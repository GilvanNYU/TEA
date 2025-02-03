from .equipment_data import EquipmentData
from .unit_operation_model import UnitOperationModel 

class UnitOperationCollection:
    def __init__(self):
        self._units: dict[str, UnitOperationModel] = {}

    @property
    def unit_operations(self) -> list[UnitOperationModel]:
        return list(self._units.values())

    def add(self, unit_name: str, equipment: EquipmentData) -> None:
        if unit_name not in self._units.keys():
            self._units[unit_name] = UnitOperationModel(unit_name)
            self._units[unit_name].add(equipment)
        else:
            self._units[unit_name].add(equipment)


    def __getitem__(self, name: str) -> UnitOperationModel:
        return self._units[name]    
    

