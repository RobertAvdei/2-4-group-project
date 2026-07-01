import numpy as np
import random
from city import City,Shelter
from warehouses import Warehouse

from roads import Road

MAP_SIZE=20

class Map:
    def __init__(self, map_size:int = MAP_SIZE):
        self.area=generate_empty_area(map_size)
        self.warehouses: list[Warehouse] = []
        self.roads: list[Road] = []
        self.cities: list[City] = []
        self.shelters: list[Shelter] = []
    
    def show(self):
        for y in self.area:
            row=[]
            for district in y:
                row.append(district.show_state())
            print('|','  '.join(row),'|')
    def get_random_coordinates(self):
        empty_roads:list[tuple[int, int]] = []
        for y in self.area:
            for district in y:
                if district.is_empty():
                    empty_roads.append(district.coordinates)
        return random.choice(empty_roads)

    def add(self, coordinates:tuple[int, int], has_city:bool= False, has_warehouse:bool= False, has_shelter:bool= False):
        y, x = coordinates
        road = Road(len(self.roads))
        self.roads.append(road)
        self.area[y][x].road = road
        
        if has_city:
            city=City(len(self.cities))
            self.cities.append(city)
            self.area[y][x].city = city
            
        if has_warehouse:
            warehouse=Warehouse(len(self.warehouses))
            self.warehouses.append(warehouse)
            self.area[y][x].warehouse = warehouse
            
        if has_shelter:
            shelter=Shelter(len(self.shelters))
            self.shelters.append(shelter)
            self.area[y][x].shelter = shelter
        
    def add_warehouse(self, supplies, vehicles,coordinates:tuple[int, int] | None= None):
        if coordinates:
            y, x = coordinates
        else:
            y, x = self.get_random_coordinates()
            
        warehouse= Warehouse (len(self.warehouses), supplies,0, vehicles)
        self.warehouses.append(warehouse)
        self.area[y][x].warehouse = warehouse

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
    
    def is_empty(self):
        if self.shelter:
            return False
        if self.city:
            return False
        if self.warehouse:
            return False
        if self.road:
            if self.road.is_blocked:
                return False
            return True
        return False
    
    def show_state(self):
        if self.shelter:
            return '\N{Tent}'
        if self.city:
            return '\N{House Building}'
        if self.warehouse:
            return '\N{Department Store}'
        if self.road:
            if self.road.is_blocked:
                return 'X '
            return'+ '
        return '  '


def generate_empty_area(map_size:int = MAP_SIZE):
    area:list[list[District]] = []
    for y in range(map_size):
        area.append([])
        for x in range(map_size):
            area[y].append(District((y,x)))
    return area


def default_map():
    map_size= MAP_SIZE
    
    default_map = Map(map_size)

    # North Small Village
    default_map.add((2,12),has_city=True)
    
    # Center Road 1
    default_map.add((1,11))
    default_map.add((2,10))
    default_map.add((3,9))
    default_map.add((4,9))
    default_map.add((5,8))
    default_map.add((6,8))
    default_map.add((7,7))
    default_map.add((8,7))
    default_map.add((9,7))
    default_map.add((10,8))
    default_map.add((11,8))
    default_map.add((12,8))
    default_map.add((13,8),has_city=True) # South Village
    
    # Center Road 2
    default_map.add((3,11))
    default_map.add((4,11))
    default_map.add((5,11))
    default_map.add((6,11))
    default_map.add((7,10))
    default_map.add((8,10))
    default_map.add((8,9),has_city=True) # Center Village
    default_map.add((8,8))
    default_map.add((9,11))
    default_map.add((10,11))
    default_map.add((11,12))
    default_map.add((12,12))
    # South Road
    default_map.add((18,14))
    default_map.add((17,13))
    default_map.add((18,12))
    default_map.add((17,11))
    default_map.add((16,11))
    default_map.add((15,10))
    default_map.add((14,9))
    default_map.add((13,9))
    default_map.add((14,7))
    default_map.add((15,6))
    default_map.add((16,5))
    default_map.add((16,4))
    default_map.add((16,3))
    
    # West Big City
    default_map.add((15,2),has_city=True)
    default_map.add((15,1),has_city=True)
    default_map.add((14,2),has_city=True)
    default_map.add((14,1),has_city=True)
    
    # West Road 1
    default_map.add((13,2))
    default_map.add((12,1))
    default_map.add((11,0))
    default_map.add((10,1))
    default_map.add((9,1))
    default_map.add((8,1))
    default_map.add((7,2))
    default_map.add((6,3))
    default_map.add((6,4),has_city=True) # West Small Village 
    default_map.add((6,5))
    default_map.add((7,6))
    
    # West Road 2
    default_map.add((13,3))
    default_map.add((12,4))
    default_map.add((11,4))
    default_map.add((10,5))
    default_map.add((9,4))
    default_map.add((8,4))
    default_map.add((7,4))
    # East road
    default_map.add((2,13))
    default_map.add((3,14))
    default_map.add((4,13))
    default_map.add((5,13))
    default_map.add((6,14))
    default_map.add((6,15))
    default_map.add((7,16))
    default_map.add((8,17))
    default_map.add((9,16))
    default_map.add((10,15))
    default_map.add((11,15))
    default_map.add((12,15))
    default_map.add((13,14))
    default_map.add((13,13))
    default_map.add((14,13))
    default_map.add((15,14))
    default_map.add((16,15))
    
    #South-East Big city
    default_map.add((17,15),has_city=True)
    default_map.add((17,16),has_city=True)
    default_map.add((17,17),has_city=True)
    default_map.add((18,15),has_city=True)
    default_map.add((18,16),has_city=True)
    default_map.add((18,17),has_city=True)
    

    # roads[1].is_blocked = True
    return default_map

# TODO
def dynamic_map():
    pass

if __name__ == "__main__":
    from warehouses_utils import create_warehouses
    supplies=100
    vehicles = 12
    
    map= default_map()
    create_warehouses(4,supplies,vehicles, map)
    map.show()

if __name__ == "__main__":
    from routing import find_optimal_route
    # Initialize the default map structure your group designed
    test_map= default_map()
    
    start_pos = (5, 2) # Core City coordinate index from your map mapping
    end_pos = (3, 3)   # Shelter coordinate index from your map mapping
    
    print("--- SIMULATING DEPLOYMENT RUN WITHOUT BLOCKAGES ---")
    route = find_optimal_route(test_map, start_pos, end_pos)
    print(f"Calculated Path: {route}")
    
    # Let's dynamically trigger an earthquake blockage on the computed path to test re-routing
    if route and len(route) > 1:
        block_coord = route[1]
        print(f"\n[AFTERSHOCK SHOCKWAVE] Road at {block_coord} collapsed!")
        
        # Insert a blocked road segment directly onto that district tile
        if test_map.area[block_coord[0]][block_coord[1]].road:
            test_map.area[block_coord[0]][block_coord[1]].road.is_blocked = True # type: ignore
        else:
            from roads import Road
            test_map.area[block_coord[0]][block_coord[1]].road = Road(id=999, is_blocked=True)
            
        print("\n--- RE-EVALUATING ALTERNATE PATH ---")
        new_route = find_optimal_route(test_map, start_pos, end_pos)
        print(f"New Adjusted Path around blockage: {new_route}")