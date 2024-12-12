from dataclasses import dataclass

@dataclass(frozen=True)
class EquipmentCostResult:
    status: dict[str, tuple[bool, str]]
    value: float
    CEPCI: float