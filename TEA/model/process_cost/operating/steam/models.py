def combustion_efficiency(flame_temp: float, stack_temp: float, ambient_temp: float) -> float:
    return (flame_temp - stack_temp)/(flame_temp - ambient_temp)
