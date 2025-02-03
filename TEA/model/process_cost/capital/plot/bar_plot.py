import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from dataclasses import dataclass
from ..result_classes.capital_cost_result import CapitalCostResult


class BarPlot:
    @dataclass(frozen=True)
    class Setting:
        ylabel: str = ''
        ytricks: tuple[float, float, int] = None

    def _setting_plot(setting: Setting) -> None:
        ax = plt.gca()
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
        plt.ylabel(setting.ylabel)
        if setting.ytricks != None:
            plt.yticks(np.arange(setting.ytricks[0], setting.ytricks[1]+setting.ytricks[2], setting.ytricks[2]))
            plt.ylim(setting.ytricks[0], setting.ytricks[1])
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles[::-1], labels[::-1], loc='upper left', bbox_to_anchor=(1, 1))
        plt.show()

    def by_area(scenarios: dict[str, CapitalCostResult], normalize_value= 1, setting: Setting = Setting()) -> None:
        fig, ax = plt.subplots()

        areas = set([area.name for scenario in scenarios.values() for area in scenario.areas])

        scenarios_labels = scenarios.keys()
        bottom = [0 for i in range(len(scenarios_labels))]

        for area in areas:
            cost = []
            for scenario in scenarios.values():
                value = sum([e.cost_result.value for up in scenario.area(area).unit_operations for e in up.equipments ])/normalize_value
                cost.append(value)
            ax.bar(scenarios_labels, cost, label=area, bottom=bottom)
            for i in range(len(scenarios_labels)):
                bottom[i] += cost[i]
            
        BarPlot._setting_plot(setting)
            
    def by_unit_operation(scenarios: dict[str, CapitalCostResult], normalize_value= 1, setting: Setting = Setting()) -> None:
        fig, ax = plt.subplots()

        unit_operations = set([f"{area.name}.{unit.name}" for scenario in scenarios.values() for area in scenario.areas for unit in area.unit_operations])
        scenarios_labels = scenarios.keys()
        bottom = [0 for i in range(len(scenarios_labels))]

        for unit in unit_operations:
            cost = []
            area_name, unit_name = unit.split('.')
            for scenario in scenarios.values():
                value = sum([equip.cost_result.value for equip in scenario.area(area_name).unit_operation(unit_name).equipments])/normalize_value
                cost.append(value)
            ax.bar(scenarios_labels, cost, label=unit, bottom=bottom)
            for i in range(len(scenarios_labels)):
                bottom[i] += cost[i]
        BarPlot._setting_plot(setting)
