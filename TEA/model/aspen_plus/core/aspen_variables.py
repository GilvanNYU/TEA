from .aspen_engine import AspenEngine

class AspenVariables:
    def __init__(self, 
                 variables: dict[str,str],
                 engine: AspenEngine):
        self._vars = variables
        self._engine = engine

    def __getitem__(self, name: str) -> float|int:
        return self._engine.get_variable(self._vars[name])
    
    def __setitem__(self, name: str, value: float|int) -> None:
        self._engine.set_variable(self._vars[name], value)

    def update(self, variables: dict[str,str]) -> None:
        self._vars = variables