from .core import AspenEngine, AspenVariables, AspenMaterialStream

class AspenSimulation:
    def __init__(self, full_path: str, 
                 variables: dict[str,str] = None, 
                 visibility=False):
        self._engine = AspenEngine(full_path, visibility)
        self._var = AspenVariables(variables, self._engine)
        self._material_streams = AspenMaterialStream(self._engine)

    @property
    def engine(self) -> AspenEngine:
        return self._engine

    @property
    def variables(self) -> AspenVariables:
        return self._var

    @property
    def material_streams(self) ->AspenMaterialStream:
        return self._material_streams
    
    def __del__(self) -> None:
        self._engine.quit()

