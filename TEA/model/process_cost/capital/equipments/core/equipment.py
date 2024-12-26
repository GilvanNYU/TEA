from abc import ABC, abstractmethod
from .equipment_result import EquipmentCostResult

class Equipment(ABC):

    @abstractmethod
    def purchased(self, size: float, CEPCI: float = 397) -> EquipmentCostResult:
        pass

    @abstractmethod
    def bare_module(self, size: float, CEPCI: float = 397) -> EquipmentCostResult:
        pass

    @abstractmethod
    def total_module(self, size: float, fraction: float = 0.18, CEPCI: float = 397) -> EquipmentCostResult:
        pass