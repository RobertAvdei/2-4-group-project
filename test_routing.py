import math
from map import default_map, Map, District
from roads import Road
from routing import find_optimal_route, heuristic

def print_visual_map(simulation_map: Map, highlighted_path: list[tuple[int, int]]| None = None):
    """
    Renders the terminal map layout while overlaying the path calculated by the router.
    """
    path_set = set(highlighted_path) if highlighted_path else set()
    map_size = len(simulation_map.area)
    
    print("   " + "  ".join(f"{x}" for x in range(map_size))) # Top column coordinates
    for y in range(map_size):
        row_chars = []
        for x in range(map_size):
            district: District = simulation_map.area[y][x]
            base_symbol = district.show_state()
            
            # If the vehicle passed through here, and it's an open area or normal road, mark it
            if (y, x) in path_set and base_symbol in [' ', '+']:
                row_chars.append('•') # Vehicle path marker
            else:
                row_chars.append(base_symbol)
                
        print(f"{y} | " + "  ".join(row_chars) + " |")

def run_comprehensive_test():
    print("=========================================")
    print("   RUNNING EOC LOGISTICS ROUTING TEST    ")
    print("=========================================\n")
    
    # Unpack default map metrics
    test_map= default_map()
    
    # Establish a start (Warehouse/City proximity) and destination (Shelter) point
    start_node = (2, 12)
    end_node = (17,15)
    
    print("[TEST 1] Rerouting Simulation on a Safe Open Map...")
    initial_path = find_optimal_route(test_map, start_node, end_node)
    print(f"-> Calculated Path Vector: {initial_path}")
    print("\nVisual Map Grid Output (Normal Condition):")
    print_visual_map(test_map, initial_path)
    
    print("\n-----------------------------------------")
    print("[TEST 2] Simulating Earthquake Structural Damage...")
    
    if initial_path and len(initial_path) > 2:
        # Dynamically place blockages right along the route cells to stress test adaptability
        critical_bottleneck = initial_path[1]
        print(f"-> Collapsing infrastructure at cell node: {critical_bottleneck}")
        
        # Inject blocked road element
        test_map.area[critical_bottleneck[0]][critical_bottleneck[1]].road = Road(id=888, is_blocked=True)
        
        print("-> Processing emergency re-evaluation around wreckage...")
        rerouted_path = find_optimal_route(test_map, start_node, end_node)
        print(f"-> Calculated Rerouted Vector: {rerouted_path}")
        
        print("\nVisual Map Grid Output (Post-Earthquake Devastation):")
        print_visual_map(test_map, rerouted_path)
            
    print("\n-----------------------------------------")
    print("[TEST 3] Total Structural Landslide/Isolation Test...")
    print("-> Sealing off all pathways accessing shelter destination (3, 3)...")
    
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            target_y = end_node[0] + dy
            target_x = end_node[1] + dx
            if (target_y, target_x) != end_node:
                test_map.area[target_y][target_x].road = Road(id=999, is_blocked=True)
                
    blocked_path = find_optimal_route(test_map, start_node, end_node)
    if blocked_path is None:
        print("[SUCCESS] Pathfinding engine safely returned 'None'. District isolation correctly flagged.")
        print("\nVisual Map Grid Output (Complete Grid Bottleneck):")
        print_visual_map(test_map, [])

if __name__ == "__main__":
    run_comprehensive_test()