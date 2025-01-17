from .enum import AspenStreamClass

class AspenStreamResult:
    def __init__(self, stream_node):
        self._vars = stream_node.Elements('Output')

    def molar_mass(self) -> float|None:
        return self._vars.Elements('MW').Value
    
    def temperature(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> float|None:
        return self._vars.Elements('TEMP_OUT').Elements(stream_class.value).Value
    
    def pressure(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> float|None:
        return self._vars.Elements('PRES_OUT').Elements(stream_class.value).Value
    
    def enthalpy_flow(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> float|None:
        return self._vars.Elements('HMX_FLOW').Elements(stream_class.value).Value
    
    def mass_flow(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> dict[str,float]|None:
        components =  self._vars.Elements('MASSFLOW').Elements(stream_class.value).Elements
        flow = {}
        for i in range(len(components)):
            value = components(i).Value
            flow[components(i).Name] = value if value != None else 0
        return flow
    
    def mass_fraction(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> dict[str,float]|None:
        flows = self.mass_flow(stream_class)
        total_flow = sum([flow for flow in flows.values()])
        fraction = {}
        for name, val in flows.items():
            fraction[name] = val/total_flow
        return fraction

    def total_mass_flow(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> float|None:
        return sum([val for val in self.mass_flow(stream_class).values()])
    
    def mass_enthalpy(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> float|None:
        return self._vars.Elements('HMX_MASS').Elements(stream_class.value).Value
    
    def molar_flow(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> dict[str,float]|None:
        if stream_class == AspenStreamClass.NC:
            return None
        
        components =  self._vars.Elements('MOLEFLOW').Elements(stream_class.value).Elements
        flow = {}
        for i in range(len(components)):
            value = components(i).Value
            flow[components(i).Name] = value if value != None else 0
        return flow
    
    def molar_fraction(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> dict[str,float]|None:
        if stream_class == AspenStreamClass.NC:
            return None
        
        flows = self.molar_flow(stream_class)
        total_flow = sum([flow for flow in flows.values()])
        fraction = {}
        for name, val in flows.items():
            fraction[name] = val/total_flow
        return fraction

    def total_molar_flow(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> float|None:
        if stream_class == AspenStreamClass.NC:
            return None
        
        return sum([val for val in self.molar_flow(stream_class).values()])
    
    def molar_enthalpy(self, stream_class: AspenStreamClass = AspenStreamClass.MIXED) -> float|None:
        if stream_class == AspenStreamClass.NC:
            return None
        
        return self._vars.Elements('HMX').Elements(stream_class.value).Value

