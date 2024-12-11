from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class EquipmentCostResult:
    status: dict[str, Tuple[bool, str]]
    value: float
    CEPCI: float