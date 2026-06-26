import random
import numpy as np
from eoc import EOC, DynamicKPIMonitor
from warehouses import Warehouse, create_warehouses, extract_structural_demands
from roads import create_roads
from main import earthquake, AFTERSHOCK_CHANCE, INITIAL_SUPPLIES, INITIAL_VEHICLES, TIME_MAX


def trace_single_simulation():
    print("\n=======================================================")
    print("       HOUR-BY-HOUR METRIC TRACE (SIMULATION RUN 0)    ")
    print("=======================================================")
    print(f"{'Hour':<6} | {'CUD (Demand)':<14} | {'CED (Equity Deficit)':<20}")
    print("-" * 55)

    # 1. Initialize our standard warehouse and road objects using your code
    warehouses = create_warehouses(4, INITIAL_SUPPLIES, INITIAL_VEHICLES)
    roads = create_roads(8)
    shock_count = 1


    # 2. Setup structural dictionaries required by the mathematical formulas
    districts_map = [w.id for w in warehouses]
    routes_map = {f"route_{r.id}": {"origin_warehouse": r.id % 4} for r in roads}
    vehicles_map = {w.id: w.vehicles for w in warehouses}

    # 3. Instantiate the EOC agent
    eoc_agent = EOC(districts_map, warehouses, routes_map, vehicles_map, time_window=TIME_MAX)

    # Setup baseline parameters for calculation layers
    structural_demands = extract_structural_demands(warehouses)
    mock_capacities = {w.id: 1000 for w in warehouses}
    mock_ideal_times = {f"route_{r.id}": 2.0 for r in roads}

    # 456460464641. Populate the initial state mapping vectors inside the agent
    for w in warehouses:
        eoc_agent.unmet_demand[w.id] = {"supplies": w.demand}
        eoc_agent.inventory[w.id] = {"supplies": w.supplies}
        eoc_agent.warehouse_status[w.id] = 1 if w.is_operational else 0

    # ---- FIX: Explicitly create a non-zero structural demand dictionary ----
    # This gives the districts baseline demands to compare deliveries against!
    structural_demands = {
        0: {"supplies": 100},
        1: {"supplies": 100},
        2: {"supplies": 100},
        3: {"supplies": 100}
    }

    # 4. Run the 72-hour timeline loop
    for h in range(TIME_MAX):
        # Trigger your exact earthquake functions
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

        # Synchronize environment transitions back into the EOC state variables
        for w in warehouses:
            eoc_agent.unmet_demand[w.id]["supplies"] = w.demand
        for r in roads:
            eoc_agent.road_status[f"route_{r.id}"] = 0 if r.is_blocked else 1

            # Record the hour state inside the monitor layer
            # FIX: Pass an intentional, unequal mock delivery layout to simulate regional unfairness
            mock_deliveries = {
                0: {
                    0: {"supplies": 80},  # District 0 gets 80% of demand met (highly favored)
                    1: {"supplies": 10},  # District 1 gets 10% of demand met (neglected)
                    2: {"supplies": 40},
                    3: {"supplies": 40}
                }
            }

            mock_active_vehicles = {f"route_{r.id}": 1 for r in roads if not r.is_blocked}
            eoc_agent.kpi_monitor.record_hour(
                h, eoc_agent.unmet_demand, mock_deliveries, mock_active_vehicles,
                eoc_agent.travel_times, mock_ideal_times, mock_capacities,
                eoc_agent.warehouse_status, structural_demands
            )

        eoc_agent.kpi_monitor.record_hour(
            h, eoc_agent.unmet_demand, mock_deliveries, mock_active_vehicles,
            eoc_agent.travel_times, mock_ideal_times, mock_capacities,
            eoc_agent.warehouse_status, structural_demands
        )

        # Print snapshot trace data at strategic tracking milestones and shock intervals
        if h % 6 == 0 or h in [14, 15, 36, 37, 71]:
            cud_val = eoc_agent.kpi_monitor.cud_trajectory[h]
            ced_val = eoc_agent.kpi_monitor.ced_trajectory[h]
            shock_note = " <- Shock 2 Window" if h == 14 else (" <- Shock 3 Window" if h == 36 else "")
            print(f"Hour {h:<2} | {cud_val:<14.2f} | {ced_val:<20.4f}{shock_note}")

    print("=======================================================")

    # Print the aggregated final scores
    totals = eoc_agent.kpi_monitor.extract_totals()
    print(f"Final Integrated CUD Total: {totals['CUD']:.2f}")
    print(f"Final Integrated CED Total: {totals['CED']:.4f}")
    #
    #
    print("=======================================================\n")


if __name__ == "__main__":
    trace_single_simulation()