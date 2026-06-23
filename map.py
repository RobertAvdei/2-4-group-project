import numpy as np
from city import City,Shelter, create_cities
from warehouses import Warehouse, create_warehouses
from roads import Road, create_roads

MAP_SIZE=20

class Map:
    def __init__(self, map_size:int = MAP_SIZE):
        self.area=generate_empty_area(map_size)
    
    def show(self):
        for y in self.area:
            row=[]
            for district in y:
                row.append(district.show_state())
            print('|','  '.join(row),'|')


class District:
    def __init__(self, coordinates:tuple[int, int],
                vulnerability_index:float = 0.0,
                warehouse:Warehouse | None = None, 
                city: City| None= None, 
                road: Road | None= None,
                shelter: Shelter | None = None):
        self.coordinates = coordinates
        self.vulnerability_index = vulnerability_index
        self.warehouse = warehouse
        self.city = city
        self.road = road
        self.shelter=shelter
        
    def show_state(self):
        if self.shelter:
            return 'S'
        if self.city:
            return 'C'
        if self.warehouse:
            return 'W'
        if self.road:
            if self.road.is_blocked:
                return 'X'
            return'+'
        return ' '


def generate_empty_area(map_size:int = MAP_SIZE):
    area:list[list[District]] = []
    for y in range(map_size):
        area.append([])
        for x in range(map_size):
            area[y].append(District((y,x)))
    return area


def default_map():
    map_size= 10
    supplies = 100
    vehicles = 10
    nr_warehouses = 4
    nr_roads = 20
    nr_cities = 2
    
    map = Map(map_size)
    warehouses = create_warehouses(nr_warehouses,supplies,vehicles)
    roads = create_roads(nr_roads)
    cities = create_cities(nr_cities)

    map.area[2][4].city=cities[0]
    map.area[2][4].road=roads[0]
    
    map.area[3][3].shelter=Shelter(0)
    map.area[3][3].road=roads[12]
    map.area[3][4].road=roads[1]
    
    map.area[4][3].road=roads[2]
    map.area[4][4].road=roads[3]
    map.area[4][5].road=roads[4]
    
    map.area[5][2].city=cities[1]
    map.area[5][2].road=roads[5]
    map.area[5][3].road=roads[6]
    map.area[5][4].road=roads[7]
    map.area[5][5].road=roads[8]
    map.area[5][6].warehouse=warehouses[0]
    map.area[5][6].road=roads[9]

    map.area[6][3].road=roads[10]
    
    map.area[7][3].warehouse=warehouses[0]
    map.area[7][3].road=roads[11]


    # roads[1].is_blocked = True
    return map, warehouses, roads


if __name__ == "__main__":
    map, warehouses, roads = default_map()
    map.show()