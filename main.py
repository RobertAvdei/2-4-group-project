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

    # for collecting the needed info
    mc_cud_totals = []
    mc_ced_totals = []
    mc_cvtd_totals = []
    mc_cwi_totals = []

    for _ in range(num_simulations):
        warehouses = create_warehouses(4, INITIAL_SUPPLIES, INITIAL_VEHICLES)
        roads = create_roads(8)
        shock_count = 1

        # Instantiate your EOC object for this specific realization path
        from eoc import EOC
        import warehouses as wh_mod

        # Build mock mappings to feed your EOC structure
        districts_map = [w.id for w in warehouses]
        routes_map = {f"route_{r.id}": {"origin_warehouse": r.id % 4} for r in roads}
        vehicles_map = {w.id: w.vehicles for w in warehouses}

        eoc_agent = EOC(districts_map, warehouses, routes_map, vehicles_map, time_window=TIME_MAX)

        # Pre-populate structural variables for calculations
        structural_demands = wh_mod.extract_structural_demands(warehouses)
        mock_capacities = {w.id: 1000 for w in warehouses}
        mock_ideal_times = {f"route_{r.id}": 2.0 for r in roads}

        # Populate initial tracking states in the state vector
        for w in warehouses:
            eoc_agent.unmet_demand[w.id] = {"supplies": w.demand}
            eoc_agent.inventory[w.id] = {"supplies": w.supplies}
            eoc_agent.warehouse_status[w.id] = 1 if w.is_operational else 0
        for r in roads:
            eoc_agent.road_status[f"route_{r.id}"] = 0 if r.is_blocked else 1
            eoc_agent.aftershock_risk[f"route_{r.id}"] = 0.1
            eoc_agent.travel_times[f"route_{r.id}"] = 3.0 if r.is_blocked else 2.0

        for h in range(TIME_MAX):
            if h == 0:
                earthquake(warehouses, roads, 20)
            if h == 14:
                if random.randrange(100) < AFTERSHOCK_CHANCE:
                    shock_count += 1
                    earthquake(warehouses, roads, 20, shock_count)
            if h == 36:
                if random.randrange(100) < AFTERSHOCK_CHANCE:
                    earthquake(warehouses, roads, 20, shock_count)
                    shock_count += 1

            # Update EOC tracking arrays based on the earthquake environment outputs
            for w in warehouses:
                eoc_agent.unmet_demand[w.id]["supplies"] = w.demand
            for r in roads:
                eoc_agent.road_status[f"route_{r.id}"] = 0 if r.is_blocked else 1

            # --- CALL MONITOR AT THE CONCLUSION OF THE HOUR CYCLE ---
            # Reset temporary hourly registry for the next clock step
            hourly_deliv = eoc_agent.hourly_deliveries_registry
            active_vehicles = {f"route_{r.id}": 1 for r in roads if not r.is_blocked}

            eoc_agent.kpi_monitor.record_hour(
                h, eoc_agent.unmet_demand, hourly_deliv, active_vehicles,
                eoc_agent.travel_times, mock_ideal_times, mock_capacities,
                eoc_agent.warehouse_status, structural_demands
            )
            eoc_agent.hourly_deliveries_registry = {}  # Flush tracking for next cycle

        # Harvest final cumulative "grades" for this specific run
        final_scores = eoc_agent.kpi_monitor.extract_totals()
        mc_cud_totals.append(final_scores["CUD"])
        mc_ced_totals.append(final_scores["CED"])
        mc_cvtd_totals.append(final_scores["CVTD"])
        mc_cwi_totals.append(final_scores["CWI"])

        unmet_demand.append(calculate_unmet_demand(warehouses))
        road_status.append(calculate_road_status(roads))

    # Optional print block to show robustness evaluation metrics on console
    print(f"\n--- ROBUSTNESS ASSESSMENT TRAJECTORIES ({num_simulations} RUNS) ---")
    print(f"Expected Cumulative Unmet Demand (Mean CUD): {np.mean(mc_cud_totals):.2f}")
    print(f"Expected Cumulative Equity Deficit (Mean CED): {np.mean(mc_ced_totals):.2f}")

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