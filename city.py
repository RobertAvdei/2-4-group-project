class City:
    def __init__(self,id:int, demand:int =0):
        self.id = id
        self.demand = demand
        
class Shelter:
    def __init__(self,id:int ,demand:int = 0, supplies:int = 0):
        self.id = id
        self.demand = demand
        self.supplies = supplies

def create_cities(amount:int):
    cities:list[City]=[]
    for i in range(amount):
        cities.append(City(i))
    return cities

def create_shelters(amount:int):
    shelters:list[Shelter]=[]
    for i in range(amount):
        shelters.append(Shelter(i))
    return shelters