import random
def split_demand(demand, splits):
    result = []
    remaining_demand = demand
    for i in range(splits):
        if i == splits-1:
            result.append(remaining_demand)
        else:
            result.append(remaining_demand- random.randint(0,remaining_demand))
            remaining_demand -= result[i]
    return result


if __name__ == "__main__":
    result = split_demand(100, 4)
    print(result)