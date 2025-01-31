from dataclasses import dataclass
from .equipments.core import Equipment

@dataclass(frozen=True)
class EquipmentForm:
    name: str
    size: float
    model: Equipment