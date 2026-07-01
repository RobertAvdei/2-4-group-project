class Warehouse:
    def __init__(self, id, supplies=0, demand=0,vehicles=0, is_operational=True):
        self.supplies = supplies
        self.id = id
        self.demand = demand
        self.vehicles = vehicles
        self.is_operational = is_operational
        # capacity?