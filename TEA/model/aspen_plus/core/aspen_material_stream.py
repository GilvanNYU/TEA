from typing import Literal
from .aspen_engine import AspenEngine


class AspenMaterialStream:
    def __init__(self, engine: AspenEngine):
        self._engine = engine

    def __getitem__(self, stream: tuple[str,Literal['MIXED', 'CISOLID', 'NC']]) -> dict[str, float|int]:
        name, stream_type  = stream
        names = name.split('.')
        end = f"\\Data\\Streams\\{names[-1]}\\Output\\"
        if len(names) == 1:
            stream_path =  end
        else:
            base = ''
            for block in names[:-1]:
                base += f'\\Data\\Blocks\\{block}'
            stream_path = base + end
        if stream_type != 'NC':
            node_mass = self._engine.find_node(stream_path + f'MASSFLOW\\{stream_type}')
            node_mole = self._engine.find_node(stream_path + f'MOLEFLOW\\{stream_type}')
            mass_flow = {}
            mole_flow = {}
            for i in range(node_mass.Elements.Count):
                comp = node_mass.Elements(i).Name
                mass = node_mass.Elements(i).Value
                mole = node_mole.Elements(i).Value
                mass_flow[comp]= mass if mass != None else 0
                mole_flow[comp]= mole if mole != None else 0
            
            stream = {
                'temperature': self._engine.find_node(stream_path + f'TEMP_OUT\\{stream_type}').Value,
                'pressure': self._engine.find_node(stream_path + f'PRES_OUT\\{stream_type}').Value,
                'enthalpy': self._engine.find_node(stream_path + f'HMX_MASS\\{stream_type}').Value,
                'molar_mass': self._engine.find_node(stream_path + 'MW').Value,
                'mass_flow': mass_flow,
                'mole_flow': mole_flow,
            }
            return stream
        else:
            node_mass = self._engine.find_node(stream_path + f'MASSFLOW\\{stream_type}')
            node_mole = self._engine.find_node(stream_path + f'MOLEFLOW\\{stream_type}')
            mass_flow = {}
            mole_flow = {}
            for i in range(node_mass.Elements.Count):
                comp = node_mass.Elements(i).Name
                mass = node_mass.Elements(i).Value
                mass_flow[comp]= mass if mass != None else 0
            
            stream = {
                'temperature': self._engine.find_node(stream_path + f'TEMP_OUT\\{stream_type}').Value,
                'pressure': self._engine.find_node(stream_path + f'PRES_OUT\\{stream_type}').Value,
                'mass_enthalpy': self._engine.find_node(stream_path + f'HMX_MASS\\{stream_type}').Value,
                'mass_flow': mass_flow,
            }
            return stream

        
