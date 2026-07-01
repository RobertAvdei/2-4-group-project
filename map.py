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
    return map, warehouses, roads, cities


# if __name__ == "__main__":
#     map, warehouses, roads = default_map()
#     map.show()

if __name__ == "__main__":
    # Unpack all 4 values properly by adding a placeholder '_' for the cities variable
    simulation_map, warehouses, roads, _ = default_map()
    
    # Render the full grid map visually in the terminal
    simulation_map.show()

# if __name__ == "__main__":
#     from routing import find_optimal_route
    
#     # Initialize the default map structure your group designed
#     test_map = default_map()
    
#     start_pos = (5, 2) # Core City coordinate index from your map mapping
#     end_pos = (3, 3)   # Shelter coordinate index from your map mapping
    
#     print("--- SIMULATING DEPLOYMENT RUN WITHOUT BLOCKAGES ---")
#     route = find_optimal_route(test_map, start_pos, end_pos)
#     print(f"Calculated Path: {route}")
    
#     # Let's dynamically trigger an earthquake blockage on the computed path to test re-routing
#     if route and len(route) > 1:
#         block_coord = route[1]
#         print(f"\n[AFTERSHOCK SHOCKWAVE] Road at {block_coord} collapsed!")
        
#         # Insert a blocked road segment directly onto that district tile
#         if test_map.area[block_coord[0]][block_coord[1]].road:
#             test_map.area[block_coord[0]][block_coord[1]].road.is_blocked = True
#         else:
#             from roads import Road
#             test_map.area[block_coord[0]][block_coord[1]].road = Road(id=999, is_blocked=True)
            
#         print("\n--- RE-EVALUATING ALTERNATE PATH ---")
#         new_route = find_optimal_route(test_map, start_pos, end_pos)
#         print(f"New Adjusted Path around blockage: {new_route}")

if __name__ == "__main__":
    from routing import find_optimal_route
    
    # 1. Unpack all 4 values properly so simulation_map gets the actual Map object
    simulation_map, warehouses, roads, _ = default_map()
    
    print("--- EMERGENCY REACTION NETWORK MATRIX LAYOUT ---")
    simulation_map.show()
    print("\n------------------------------------------------")
    
    # Coordinates based on your printed map locations
    start_pos = (5, 2)  # Starting location
    end_pos = (3, 3)    # Target shelter
    
    print("--- SIMULATING DEPLOYMENT RUN WITHOUT BLOCKAGES ---")
    # Pass the correctly unpacked simulation_map here
    route = find_optimal_route(simulation_map, start_pos, end_pos)
    print(f"Calculated Path: {route}")
    
    # 2. Let's dynamically test an aftershock blockage on the computed path
    if route and len(route) > 1:
        block_coord = route[1]
        print(f"\n[AFTERSHOCK SHOCKWAVE] Road at {block_coord} collapsed!")
        
        # Inject a blocked road object directly onto that cell
        if simulation_map.area[block_coord[0]][block_coord[1]].road:
            simulation_map.area[block_coord[0]][block_coord[1]].road.is_blocked = True
        else:
            from roads import Road
            simulation_map.area[block_coord[0]][block_coord[1]].road = Road(id=999, is_blocked=True)
            
        print("\n--- RE-EVALUATING ALTERNATE PATH ---")
        new_route = find_optimal_route(simulation_map, start_pos, end_pos)
        print(f"New Adjusted Path around blockage: {new_route}")