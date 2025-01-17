from .enum import AspenAttribute
from .aspen_stream_result import AspenStreamResult
from .aspen_engine import AspenEngine

def add_stream(data_node, stream_map: dict, base: str):
    streams = data_node.Elements('Streams')
    for i in range(len(streams.Elements)):
        stream = streams.Elements(i)
        if stream.AttributeValue(AspenAttribute.RECORD_TYPE.value) == 'MATERIAL':
            stream_map[base+stream.Name] = AspenStreamResult(stream)

def mapping_hierarchy_streams(blocks_node, stream_map: dict, base: str):
    for i in range(len(blocks_node)):
        if 'Hierarchy' == blocks_node(i).AttributeValue(AspenAttribute.RECORD_TYPE.value):
            name = blocks_node(i).Name
            data_node = blocks_node(i).Elements('Data')
            add_stream(data_node, stream_map, base + name + '.')
            mapping_hierarchy_streams(data_node.Elements('Blocks').Elements, stream_map, base + name + '.')

def mapping_streams(engine: AspenEngine) -> dict[str, AspenStreamResult]:
    stream_map = {}
    data_node = engine.find_node('\\Data')
    add_stream(data_node, stream_map, '')
    blocks_node = data_node.Elements('Blocks').Elements
    mapping_hierarchy_streams(blocks_node, stream_map, '')
    return stream_map