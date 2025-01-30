import math

def heat_exchanger_size(Q, Thin, Thout, Tcin, Tcout, U) -> float:
    '''
    Q: Heat duty (kW)\n
    Thin: Inlet temperature hot stream (degree)\n
    Thout Outlet temperature hot stream (degree)\n
    Tcin: Inlet temperature cold stream (degree)\n
    Tcout: Outlet temperature cold stream (degree)\n
    U: Global coefficient (kW/(m2.degree))\n
    return: area (m2)
    '''
    lmtd = ((Thin - Tcout) - (Thout - Tcin))/(math.log((Thin - Tcout)/(Thout - Tcin)))
    return abs(Q)/(U*lmtd)

def vessel_size(liq_flow: float, res_time: float) -> float:
    '''
    liq_flow: liquid volumetric flow (m3/h)\n
    res_time: liquid residence time (h)\n
    return: volume (m3)
    '''
    return liq_flow*res_time

def column_size(num_stage: float, diameter: float, tray_space: float) -> float:
    '''
    num_stage: number of stages (-)\n
    diameter: diameter of column (m)\n
    tray_space: tray space (m)\n
    return: volume (m3)
    '''
    return tray_space*(num_stage/0.75)*math.pi*((diameter/2)**2)