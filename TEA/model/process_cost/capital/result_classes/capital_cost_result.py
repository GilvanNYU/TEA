from .area_result import AreaResult


class CapitalCostResult:
    def __init__(self):
       self._areas: dict[str, AreaResult] = {}

    @property
    def areas(self) -> list[AreaResult]:
        return list(self._areas.values())
    
    def area(self, name: str) -> AreaResult:
        return self._areas[name]
    
    def create_area(self, name: str) -> None:
        self._areas[name] = AreaResult(name)

