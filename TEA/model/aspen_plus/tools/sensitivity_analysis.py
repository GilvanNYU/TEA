from itertools import product
from dataclasses import dataclass
from ..aspen_simulation import AspenSimulation

@dataclass(frozen=True)
class SensitivityAnalysisResults:
    status: tuple[bool, str]
    variables: dict[str, float|int]
    tracked: dict[str, float|int]

def sensitivity_analysis(aspen: AspenSimulation, 
                         sensitivy_var: dict[str,list[float|int]],
                         tracked_var: list[str],
                         reinitiate: bool = False) -> list[SensitivityAnalysisResults]:
    if reinitiate:
        aspen.engine.reinitiate()
        
    scenarios = []
    for variables in product(*[sensitivy_var[v] for v in sensitivy_var]):
        scenario = {}
        for i, var_name in enumerate(sensitivy_var.keys()):
            scenario[var_name] = variables[i]
        scenarios.append(scenario)
    sensitivy = []
    for scenatio in scenarios:
        for var_name in scenatio:
            aspen.variables[var_name] = scenatio[var_name]
            
        aspen.run()
        status = aspen.engine.run_status()

        tracked = {}
        for tracked_name in tracked_var:
            tracked[tracked_name] = aspen.variables[tracked_name]

        sensitivy.append(
            SensitivityAnalysisResults(status=status,
                                       variables=scenatio,
                                       tracked=tracked))
    
    return sensitivy