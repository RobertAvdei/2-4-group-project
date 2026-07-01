import heapq
import math
from map import Map, District

def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    """
    Calculates Octile distance between point a and point b.
    This is the exact shortest possible mathematical metric on a grid 
    where diagonal movement is allowed.
    """
    dy = abs(a[0] - b[0])
    dx = abs(a[1] - b[1])
    # cost of straight lines is 1, cost of diagonal is sqrt(2) ~ 1.414
    return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

def find_optimal_route(simulation_map: Map, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]] | None:
    """
    Finds the shortest passable path from a start coordinate to an end coordinate 
    using A* supporting 8-directional movement (orthogonal + diagonal).
    Returns a list of coordinates representing the path, or None if no passable route exists.
    """
    map_size = len(simulation_map.area)
    
    # Priority Queue elements: (f_score, current_coordinate)
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    # Tracking structural dictionaries
    came_from = {}
    g_score = {start: 0.0}
    f_score = {start: heuristic(start, end)}
    
    # 8-Directional grid movement: (dy, dx, movement_cost)
    directions = [
        # Cardinal / Orthogonal moves (Cost = 1.0)
        (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
        # Diagonal moves (Cost = sqrt(2) ~ 1.414)
        (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)), 
        (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))
    ]
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        # Goal reached: Reconstruct the path backwards
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
            
        for dy, dx, movement_cost in directions:
            neighbor = (current[0] + dy, current[1] + dx)
            
            # 1. Bounds Constraint check
            if not (0 <= neighbor[0] < map_size and 0 <= neighbor[1] < map_size):
                continue
                
            district: District = simulation_map.area[neighbor[0]][neighbor[1]]
            
            # 2. Blockage Constraint check: 
            # The tile MUST have a road to be drivable. If there is no road, OR if the road is blocked, skip it.
            if not district.road or district.road.is_blocked:
                continue
                
            # Dynamic Step Cost evaluation based on vector geometry
            tentative_g_score = g_score[current] + movement_cost
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                
                # Check if neighbor is already in open_set queue manually 
                if not any(item[1] == neighbor for item in open_set):
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    
    return None # Return None if blocked entirely

