import random

class Warehouse:
    def __init__(self, id, supplies=0, demand=0,vehicles=0, is_operational=True):
        self.supplies = supplies
        self.id = id
        self.demand = demand
        self.vehicles = vehicles
        self.is_operational = is_operational
        # capacity?
        

def create_warehouses(amount:int, supplies, vehicles):
    warehouses:list[Warehouse]=[]
    split_supplies = supplies/amount # assuming equal initial distribution
    split_vehicles = vehicles/amount
    for i in range(amount):
        warehouses.append(Warehouse(i,split_supplies,0,split_vehicles))
    return warehouses

def calculate_unmet_demand(warehouses:list[Warehouse]):
    unmet_demand=0
    for w in warehouses:
        unmet_demand+= max(w.demand - w.supplies, 0) # if there are more supplies than demand, add 0
    return unmet_demand

def split_demand(demand, splits):
    result = []
    remaining_demand = demand
    for i in range(splits):
        if i == splits-1:
            result.append(remaining_demand)
        else:
            result.append(remaining_demand- random.randint(0,remaining_demand))
            remaining_demand -= result[i]
    return result


if __name__ == "__main__":
    result = split_demand(100, 4)
    print(result)