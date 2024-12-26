class LaborCost:
    def __init__(self, salary: float, num_shift: int = 3, work_days: int = 245):
        """
        salary ($/year) - annual salary\n
        num_shift: number of shift per day\n
        work_days (day/year): work days in the year
        """
        self._salary = salary
        self._operator_factor = num_shift*365/work_days

    def number_operators(self, solid_steps: int, non_solid_steps: int) -> int:
        """
        solid_steps - process steps involving handling solids (transport, partical size control, particulate removal)\n
        non_solid_steps - number of process steps not invloving handling solids, including compression, heating, cooling, mixing, separation and reaction, but not including pumps and vessels\n
        return - number of operators,
        """
        return int(self._operator_factor*(6.29 + 31.7*(solid_steps)**2 + 0.23*non_solid_steps)**0.5)
    
    def cost(self, solid_steps: int, non_solid_steps: int) -> float:
        """
        solid_steps - process steps involving handling solids (transport, partical size control, particulate removal)\n
        non_solid_steps - number of process steps not invloving handling solids, including compression, heating, cooling, mixing, separation and reaction, but not including pumps and vessels\n
        return ($/year)- labor cost,
        """
        return self.number_operators(solid_steps, non_solid_steps)*self._salary