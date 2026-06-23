import numpy as np

class EOC:
    def __init__(self, districts, warehouses, routes, initial_vehicles, time_window=72):
        """
        Initializes the Emergency Operations Center state vector.
        """
        # System boundaries & definitions
        self.districts = districts      # List/Dict of districts
        self.warehouses = warehouses  # List/Dict of warehouses
        self.routes = routes          # List/Dict of route mappings
        
        # --- STATE VECTOR STATE VARIABLES (st) ---
        # ud_s_t: Unmet demand per district per supply type {district_id: {supply_type: quantity}}
        self.unmet_demand = {} 
        
        # I_w_s_t: Current remaining supplies at warehouse {warehouse_id: {supply_type: quantity}}
        self.inventory = {} 
        
        # b_r_t: Passable roads indicator {route_id: 1 if passable, 0 if blocked}
        self.road_status = {} 
        
        # v_w_t: Available vehicles currently at warehouse {warehouse_id: count}
        self.available_vehicles = initial_vehicles # Usage of provided vehicle data, instead of empty dictionary, to track total fleet availability across all warehouses. 
        
        # RT_t: Remaining time out of the 72-hour window
        self.remaining_time = float(time_window) 
        
        # o_w_t: Operational status of warehouses {warehouse_id: 1 if active, 0 if damaged/closed}
        self.warehouse_status = {} 
        
        # Ar_t: Active aftershock risk level per route {route_id: value between 0.0 and 1.0}
        self.aftershock_risk = {} 

        # --- SYSTEM CONSTANTS & SCENARIO THRESHOLDS ---
        self.A_max = 0.7  # Critical risk threshold (from research)
        self.travel_times = {} # Expected travel times {route_id: hours}

    def dispatch(self, w, d, s, r, n, quantity):
        """
        Action: Sends n vehicles with supplies s from warehouse w to district d along route r.
        Feasible when: Route is open, inventory > 0, vehicles available, time permits, 
                       warehouse is active, and aftershock risk < critical threshold.
        """
        # Evaluation of feasibility constraints
        is_passable = self.road_status.get(r, 0) == 1
        has_inventory = self.inventory.get(w, {}).get(s, 0) >= quantity
        has_vehicles = self.available_vehicles.get(w, 0) >= n
        time_permits = self.remaining_time >= self.travel_times.get(r, 0)
        is_operational = self.warehouse_status.get(w, 0) == 1
        risk_acceptable = self.aftershock_risk.get(r, 0.0) < self.A_max

        if is_passable and has_inventory and has_vehicles and time_permits and is_operational and risk_acceptable:
            # Execute State Modifications
            self.inventory[w][s] -= quantity  # Decreases inventory by amount dispatched
            self.available_vehicles[w] -= n   # Decreases vehicles at warehouse w by n
            
            # Decreases unmet demand (capped at 0 via system transition max(0, ud - z))
            self.unmet_demand[d][s] = max(0, self.unmet_demand[d].get(s, 0) - quantity)
            
            print(f"[ACTION SUCCESS] Dispatched {n} vehicles moving {quantity}kg of {s} from {w} to {d} via {r}.")
            return True
        else:
            print(f"[ACTION FAILED] Dispatch({w}->{d}) rejected. Constraints violated.")
            return False

    def reroute(self, v, r, r_prime):
        """
        Action: Redirects a vehicle v from a newly blocked route r to an alternate route r_prime.
        Feasible when: Current route r is blocked (0), alternate route r_prime is passable (1), 
                       and alternate route risk <= critical threshold.
        """
        current_blocked = self.road_status.get(r, 1) == 0
        alternate_passable = self.road_status.get(r_prime, 0) == 1
        alternate_risk_ok = self.aftershock_risk.get(r_prime, 0.0) <= self.A_max

        if current_blocked and alternate_passable and alternate_risk_ok:
            self.vehicle_routes[v] = r_prime  # Update vehicle's route to the alternate path
            # State update: remaining time is pressurized by added detour duration
            additional_time = max(0, self.travel_times.get(r_prime, 0) - self.travel_times.get(r, 0))
            self.remaining_time -= additional_time # Deducts detour time from 72-hour window
            # Note: Total remaining time simulation updates globally, but this tracks immediate operational pressure
            print(f"[ACTION SUCCESS] Rerouted vehicle off blocked path {r} onto viable alternate path {r_prime}.")
            return True
        else:
            print(f"[ACTION FAILED] Rerouting from {r} to {r_prime} is structurally unfeasible.")
            return False

    def prioritise(self, d, epsilon_thresholds, prioritized_routes_map):
        """
        Action: Forcefully routes asset capacity to a district whose unmet demand breaches the tolerable policy threshold.
        Feasible when: Unmet demand breaches policy epsilon, at least one route to d is open, 
                       and inventory & vehicles are non-zero.
        """
        triggered = False
        
        # Check if any supply type in the district violates the policy threshold (ud > epsilon)
        for supply_type, current_unmet in self.unmet_demand.get(d, {}).items():
            epsilon = epsilon_thresholds.get(d, {}).get(supply_type, 0)
            
            if current_unmet > epsilon:
                # Target the feasible pathways servicing this specific district
                for r in prioritized_routes_map.get(d, []):
                    w = self.routes.get(r, {}).get('origin_warehouse')
                    
                    if (self.road_status.get(r, 0) == 1 and 
                        self.available_vehicles.get(w, 0) > 0 and 
                        self.inventory.get(w, {}).get(supply_type, 0) > 0):
                        
                        # Calculate allocation to bring demand down exactly to epsilon parameters
                        required_allocation = current_unmet - epsilon
                        available_stock = self.inventory[w][supply_type]
                        dispatch_amount = min(required_allocation, available_stock)
                        
                        # Prioritized action executes via base dispatch architecture
                        self.dispatch(w, d, supply_type, r, n=1, quantity=dispatch_amount)
                        triggered = True
                        break # Break route loop once an active supply run is pushed
        return triggered

    def hold(self, w):
        """
        Action: Suspends and freezes all fleet departures sitting at warehouse w.
        Feasible when: The regional aftershock risk surrounding the facility meets or exceeds safety bounds.
        """
        # Check if any adjacent routes from warehouse w have crossed critical threshold bounds
        high_risk_detected = any(
            self.aftershock_risk.get(r, 0.0) >= self.A_max 
            for r in self.routes if self.routes[r].get('origin_warehouse') == w
        )

        if high_risk_detected:
            # Action Execution: Forces all vehicle parameters to remain static at depot. Nothing changes.
            print(f"[ACTION SAFETY HOLD] Severe aftershock activity at {w}. All vehicle dispatches frozen.")
            return True
        return False

    def reallocate(self, w, w_prime, s, quantity):
        """
        Action: Transfers internal bulk emergency supplies of type s from safe warehouse w to under-stocked warehouse w_prime.
        Feasible when: Both facilities are active, origin inventory has sufficient stock, 
                       vehicles are available to execute transfer, and connecting route is clear.
        """
        both_active = self.warehouse_status.get(w, 0) == 1 and self.warehouse_status.get(w_prime, 0) == 1
        has_stock = self.inventory.get(w, {}).get(s, 0) >= quantity
        has_transport = self.available_vehicles.get(w, 0) > 0
        
        # Assuming direct infrastructure route exists between depots
        connecting_route = f"route_{w}_{w_prime}"
        route_clear = self.road_status.get(connecting_route, 0) == 1

        if both_active and has_stock and has_transport and route_clear:
            # Execute state transformation logic
            self.inventory[w][s] -= quantity         # Decreases stock at w
            self.inventory[w_prime][s] = self.inventory[w_prime].get(s, 0) + quantity # Increases stock at w'
            
            print(f"[ACTION SUCCESS] Interlink Resource Transfer: Shifted {quantity}kg of {s} from {w} to {w_prime}.")
            return True
        else:
            print(f"[ACTION FAILED] Warehouse-to-Warehouse transfer rejected.")
            return False

    def activate_warehouse(self, w_prime, damaged_w):
        """
        Action: Opens an inactive backup warehouse (w_prime) to seamlessly replace a collapsed/damaged terminal (damaged_w).
        Feasible when: Primary warehouse is damaged (0) and backup facility has available resources & inventory tracking.
        """
        primary_destroyed = self.warehouse_status.get(damaged_w, 1) == 0
        backup_exists = w_prime in self.warehouse_status and self.warehouse_status[w_prime] == 0
        backup_has_stock = sum(self.inventory.get(w_prime, {}).values()) > 0

        if primary_destroyed and backup_exists and backup_has_stock:
            # Update state parameters
            self.warehouse_status[w_prime] = 1 # Becomes fully operational for regional distribution
            print(f"[ACTION SUCCESS] Contingency Plan Triggered: Activated reserve facility {w_prime} to offset failure at {damaged_w}.")
            return True
        else:
            print(f"[ACTION FAILED] Contingency activation requirement parameters not met.")
            return False