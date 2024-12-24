from TEA.model.process_cost.equipments import EvaporatorCost, EvaporatorProperties

evap_pro = EvaporatorProperties(EvaporatorProperties.Material.CarbonSteel, 
                                EvaporatorProperties.Model.ForcedCirculation, 
                                10)
evap = EvaporatorCost(evap_pro)

print(evap.total_module(100))