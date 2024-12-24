from dataclasses import dataclass
from .model.process_cost.equipments.core import Equipment

@dataclass(frozen=True)
class EquipmentDatasheet:
    equipment: Equipment
    size: float

class EquipmentCatalog:
    def __init__(self, CEPCI):
        self._CEPCI = CEPCI
        self._datasheet : dict[str, EquipmentDatasheet] = {}

    def add(self, name:str, datasheet: EquipmentDatasheet) -> None:
        self._datasheet[name] = datasheet

    # def sum_bare_module(self) -> float:
    #     _sum = 0
    #     for key in self._datasheet:
    #         datasheet = self._datasheet[key]
    #         _sum += datasheet.equipment.bare_module(datasheet.size, self._CEPCI)
    #     return _sum

    # def total_module(self, factor : float = 0.18) -> float:
    #     return (1 + factor)*self.sum_bare_module()