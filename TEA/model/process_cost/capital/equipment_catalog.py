from dataclasses import dataclass
from .equipments.core import EquipmentCostResult
from .equipments.core import Equipment

@dataclass(frozen=True)
class EquipmentDatasheet:
    name: str
    equipment: Equipment
    size: float

class EquipmentCatalog:
    def __init__(self, fee_fract: float, CEPCI: float):
        self._fee_fract = fee_fract
        self._CEPCI = CEPCI
        self._datasheet : dict[str, EquipmentDatasheet] = {}

    def add(self, datasheet: EquipmentDatasheet) -> None:
        self._datasheet[datasheet.name] = datasheet

    def purchased(self) -> dict[str, float| dict[str, EquipmentCostResult|EquipmentDatasheet]]:
        summary : dict[str, float| dict[str, EquipmentCostResult|EquipmentDatasheet]] = {'equipments':{}, 'total': 0.0}
        for name in self._datasheet:
            datasheet = self._datasheet[name]
            cost = datasheet.equipment.purchased(datasheet.size, self._CEPCI)
            summary['equipments'][name] = {
                'datasheet': datasheet,
                'cost': cost
            }
            summary['total'] += cost.value
        return summary

    def bare_module(self) -> float:
        summary : dict[str, float| dict[str, EquipmentCostResult|EquipmentDatasheet]] = {'equipments':{}, 'total': 0.0}
        for name in self._datasheet:
            datasheet = self._datasheet[name]
            cost = datasheet.equipment.bare_module(datasheet.size, self._CEPCI)
            summary['equipments'][name] = {
                'datasheet': datasheet,
                'cost': cost
            }
            summary['total'] += cost.value
        return summary

    def total_module(self) -> float:
        summary : dict[str, float| dict[str, EquipmentCostResult|EquipmentDatasheet]] = {'equipments':{}, 'total': 0.0}
        for name in self._datasheet:
            datasheet = self._datasheet[name]
            cost = datasheet.equipment.total_module(datasheet.size, self._fee_fract, self._CEPCI)
            summary['equipments'][name] = {
                'datasheet': datasheet,
                'cost': cost
            }
            summary['total'] += cost.value
        return summary