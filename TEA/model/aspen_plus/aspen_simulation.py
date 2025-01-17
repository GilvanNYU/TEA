from .core import AspenEngine, AspenVariables, AspenStreams

class AspenSimulation:
    def __init__(self, full_path: str, 
                 variables: dict[str,str] = None, 
                 visibility=False):
        self._engine = AspenEngine(full_path, visibility)
        self._var = AspenVariables(variables, self._engine)
        self._streams = AspenStreams(self._engine)

    @property
    def engine(self) -> AspenEngine:
        return self._engine

    @property
    def variables(self) -> AspenVariables:
        return self._var

    @property
    def streams(self) ->AspenStreams:
        return self._streams
    
    def initialize(self) -> None:
        self._engine.run()
        self._streams.initialize()


    def __del__(self) -> None:
        self._engine.quit()

