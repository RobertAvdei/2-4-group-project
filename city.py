

class City:
    def __init__(self,id:int):
        self.id = id
        
    

class Shelter:
    def __init__(self,id:int):
        self.id = id

def create_cities(amount:int):
    cities:list[City]=[]
    for i in range(amount):
        cities.append(City(i))
    return cities