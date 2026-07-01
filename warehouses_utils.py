from warehouses import Warehouse
from map import Map     

def create_warehouses(amount:int, supplies, vehicles,map:Map):
    split_supplies = supplies/amount # assuming equal initial distribution
    split_vehicles = vehicles/amount
    for i in range(amount):
        map.add_warehouse(supplies=split_supplies,vehicles=split_vehicles)


def calculate_unmet_demand(map:Map):
    unmet_demand=0
    warehouses = map.warehouses
    shelters = map.shelters
    for w in warehouses:
        unmet_demand+= max(w.demand - w.supplies, 0) # if there are more supplies than demand, add 0
    for s in shelters:
        unmet_demand+= max(s.demand - s.supplies, 0)
    return unmet_demand
