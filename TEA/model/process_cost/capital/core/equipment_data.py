from dataclasses import dataclass
from ..equipments.core import EquipmentCost


@dataclass(frozen=True)
class EquipmentData:
    name: str
    size: float
    model: EquipmentCost
