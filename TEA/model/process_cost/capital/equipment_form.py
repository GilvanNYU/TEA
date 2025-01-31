from dataclasses import dataclass
from .equipments.core import EquipmentCost

@dataclass(frozen=True)
class EquipmentForm:
    name: str
    size: float
    model: EquipmentCost