from dataclasses import dataclass
from typing import tuple

@dataclass(frozen=True)
class PressureFactorResult:
    status: tuple[bool, str]
    value: float