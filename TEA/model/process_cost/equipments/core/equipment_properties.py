from dataclasses import dataclass

@dataclass(frozen=True)
class EquipmentProperties:
    data: tuple[float, float, float]
    unit: str
    min_size: float
    max_size: float