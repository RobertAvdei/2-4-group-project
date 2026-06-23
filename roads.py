class Road:
    def __init__(self,id,is_blocked=False):
        self.is_blocked = is_blocked
        self.id = id
        # aftershock?

def create_roads(amount:int):
    roads:list[Road]=[]
    for i in range(amount):
        roads.append(Road(i))
    return roads


def calculate_road_status(roads:list[Road]):
    blocked_roads = 0
    for r in roads:
        blocked_roads += 1 if r.is_blocked else 0
    return blocked_roads/len(roads) * 100