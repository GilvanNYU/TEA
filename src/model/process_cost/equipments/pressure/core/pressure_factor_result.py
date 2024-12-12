from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class PressureFactorResult:
    status: Tuple[bool, str]
    value: float