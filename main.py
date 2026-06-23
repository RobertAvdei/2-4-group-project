from warehouses import Warehouse, create_warehouses, calculate_unmet_demand, split_demand
from roads import Road, create_roads, calculate_road_status
import random
import matplotlib.pyplot as plt
import numpy as np

TIME_MAX = 72
INITIAL_SUPPLIES = 100
INITIAL_VEHICLES = 12
DEMAND_MEAN = 60
DEMAND_DEVIATION = 10
NUM_SIMULATIONS = 10000 
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
        warehouses = create_warehouses(4,INITIAL_SUPPLIES,INITIAL_VEHICLES)
        roads = create_roads(8)
        shock_count = 1
        for h in range(TIME_MAX):
            if h==0:
                earthquake(warehouses, roads,20)
            if h==14:
                if random.randrange(100) < AFTERSHOCK_CHANCE:
                    shock_count +=1
                    earthquake(warehouses, roads,20,shock_count)
                    
            if h==36:
                if random.randrange(100) < AFTERSHOCK_CHANCE:
                    earthquake(warehouses, roads,20,shock_count)
                    shock_count +=1

            # Actions that start and conclude the same hour
            
            # Actions that start this hour but conclude later
            
            # Solve Actions
            
        unmet_demand.append(calculate_unmet_demand(warehouses))
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