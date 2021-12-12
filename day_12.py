import os
from collections import defaultdict


# Read in data and build dictionary mapping each cave to a list of its connected caves
connections = defaultdict(list)
with open(os.path.join('data', 'day_12.txt'), 'r') as f:
    for line in f.readlines():
        cave_1, cave_2 = line.strip().split('-')
        connections[cave_1].append(cave_2)
        connections[cave_2].append(cave_1)


def explore_part_1(route):
    """Recursively explore connected caves to find all valid routes."""
    current = route[-1]
    if current == 'end':
        routes.append(route)
    else:
        connected_caves = connections[current]
        for cave in connected_caves:
            if cave.isupper() or cave not in route:
                explore_part_1(route + [cave])


routes = []
explore_part_1(['start'])
print(f'Part 1 Solution: {len(routes)}')


def explore_part_2(route):
    """Recursively explore connected caves to find all valid routes with one permitted exception."""
    current = route[-1]
    if current == 'end':
        routes.append(route)
    else:
        connected_caves = connections[current]
        for cave in connected_caves:
            if cave.isupper() or cave not in route:
                explore_part_2(route + [cave])
            elif cave == exception and route.count(cave) < 2:
                explore_part_2(route + [cave])


routes = []
exceptions = [cave for cave in connections if cave not in ('start', 'end') and cave.islower()]
for exception in exceptions:
    explore_part_2(['start'])
print(f'Part 2 Solution: {len(set(str(route) for route in routes))}')
