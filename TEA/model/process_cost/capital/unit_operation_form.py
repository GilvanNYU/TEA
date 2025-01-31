from .equipment_form import EquipmentForm

class UnitOperationForm:
    def __init__(self, name: str):
        self._name = name
        self._operations: dict[str,list[EquipmentForm]] = {}

    @property
    def name(self) -> str:
        return self._name

    def add(self, operation_name: str, unit_operation: list[EquipmentForm]|EquipmentForm) -> None:
        if operation_name not in self._operations.keys():
            self._operations[operation_name] = []

        if type(list()) == type(unit_operation):
            for equip in unit_operation:
                self._operations[operation_name].append(equip)
        else:
            self._operations[operation_name].append(unit_operation)       

    def unit_operation(self, name: str) -> list[EquipmentForm]:
        return self._operations[name]
    
    def unit_operations(self) -> list[tuple[str,list[EquipmentForm]]]:
        return list(self._operations.items())


    

