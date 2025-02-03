from .unit_operation_collection import UnitOperationCollection
from .unit_operation_model import UnitOperationModel 
from .equipment_data import EquipmentData

class AreaModel:
    def __init__(self, name):
        self._name = name
        self._unit_collection = UnitOperationCollection()

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def unit_operations(self) -> list[UnitOperationModel]:
        return self._unit_collection.unit_operations
    
    def unit_operation(self, name: str) -> UnitOperationModel:
        return self._unit_collection[name]

    def add_equipment(self, unit_operation: str, equipment: EquipmentData) -> None:
        self._unit_collection.add(unit_operation, equipment)

    
    
  