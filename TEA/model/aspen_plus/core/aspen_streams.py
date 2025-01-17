from .aspen_engine import AspenEngine
from .aspen_stream_result import AspenStreamResult
from .utils import mapping_streams

class AspenStreams:
    def __init__(self, engine: AspenEngine):
        self._engine = engine
        self._map = None

    def initialize(self) -> None:
        self._map = mapping_streams(self._engine)

    def is_stream(self, stream_name: str) -> bool:
        if self._map == None:
            return None
        return stream_name in self._map.keys()

    def names(self) -> list[str]:
        if self._map == None:
            return None
        return self._map.keys()

    def __getitem__(self, stream_name:str) -> AspenStreamResult:
        return self._map[stream_name]

        
