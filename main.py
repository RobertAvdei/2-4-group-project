from routing import find_optimal_route
from warehouses import Warehouse
from warehouses_utils import create_warehouses, calculate_unmet_demand
from city_utils import split_demand
from roads import Road, calculate_road_status
import random
import matplotlib.pyplot as plt
import numpy as np
from map import default_map

TIME_MAX = 72
INITIAL_SUPPLIES = 100
INITIAL_VEHICLES = 12
DEMAND_MEAN = 60
DEMAND_DEVIATION = 10
NUM_SIMULATIONS = 10000
ROAD_DAMAGE = 20
AFTERSHOCK_CHANCE = 40 # Discuss


rng = np.random.default_rng()
# road_damage is the probability of a Road being blocked
def earthquake(warehouses:list[Warehouse], roads: list[Road], road_damage, shock_count =1):
    demand = round(rng.normal(DEMAND_MEAN,DEMAND_DEVIATION)/shock_count) # Discuss
    split = split_demand(demand, len(warehouses))
    for i, w in enumerate(warehouses):
        w.demand += split[i]
    for r in roads:
        if random.randrange(100) < road_damage:
            r.is_blocked = True

def run_simulation(num_simulations):
    unmet_demand = []
    road_status = []
    for _ in range(num_simulations):
        # Initialize the grid map for routing analysis
        sim_map= default_map()

        create_warehouses(4,INITIAL_SUPPLIES,INITIAL_VEHICLES, sim_map)
        roads = sim_map.roads
        shock_count = 1
        # Establish vehicle tracker configurations
        active_dispatches = [{"start": (5, 2), "destination": (3, 3), "id": 1}]
        
        for h in range(TIME_MAX):
            if h==0:
                earthquake(sim_map.warehouses, roads,ROAD_DAMAGE)
            if h==14:
                if random.randrange(100) < AFTERSHOCK_CHANCE:
                    shock_count +=1
                    earthquake(sim_map.warehouses, roads,ROAD_DAMAGE,shock_count)
                    
            if h==36:
                if random.randrange(100) < AFTERSHOCK_CHANCE:
                    earthquake(sim_map.warehouses, roads,ROAD_DAMAGE,shock_count)
                    shock_count +=1

            # # 3. Process the vehicle movements along the map coordinates hourly
            # for vehicle in active_dispatches:
            #     path = find_optimal_route(sim_map, vehicle["start"], vehicle["destination"])
                
            #     if path is None or len(path) < 2:
            #         print(f"Hour {h}: Vehicle {vehicle['id']} blocked! No passable pathways remain.")
            #     else:
            #         next_position = path[1]
            #         print(f"Hour {h}: Vehicle {vehicle['id']} safely processed from {vehicle['start']} -> {next_position}")
            #         vehicle["start"] = next_position 

            # Actions that start and conclude the same hour
            
            # Actions that start this hour but conclude later

            # Solve Actions
        print(' ')
        sim_map.show()
        unmet_demand.append(calculate_unmet_demand(sim_map))
        road_status.append(calculate_road_status(roads))
    return unmet_demand, road_status



def main():
    unmet_demand, road_status = run_simulation(NUM_SIMULATIONS)

    plt.hist(unmet_demand, bins=50, color='skyblue', edgecolor='black')
    plt.title('Monte Carlo Simulation: Unmet Demand Distribution')
    plt.xlabel('Unmet Demand')
    plt.ylabel('Frequency')
    plt.show()
    
    plt.hist(road_status, bins=50, color='skyblue', edgecolor='black')
    plt.title('Monte Carlo Simulation: Road status Distribution')
    plt.xlabel('Road status')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    main()