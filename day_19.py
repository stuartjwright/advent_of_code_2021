from itertools import permutations, product, combinations, chain
import numpy as np
import os


def get_data():
    with open(os.path.join('data', 'day_19.txt'), 'r') as f:
        data = f.readlines()
    scanners = []
    scanner = []
    for line in data:
        if not line.strip():
            scanners.append(scanner)
        elif line.startswith('---'):
            scanner = []
        else:
            x, y, z = map(int, line.strip().split(','))
            scanner.append((x, y, z))
    scanners.append(scanner)
    return scanners


all_scanners = get_data()

scanner0 = all_scanners[0]
scanner1 = all_scanners[1]


directions_perms = np.array(list(product([1, -1], repeat=3)))
indices_perms = np.array(list(permutations(range(3), 3)))


def pairwise_distances(scanner):
    distances = {}
    for b1, b2 in combinations(scanner, 2):
        distance = (abs(b1[0] - b2[0]), abs(b1[1] - b2[1]), abs(b1[2] - b2[2]))
        distances[(b1, b2)] = distance
    return distances


distances0 = pairwise_distances(scanner0)
for indices in indices_perms:
    for directions in directions_perms:
        rotated = [(
            b[indices[0]] * directions[0],
            b[indices[1]] * directions[1],
            b[indices[2]] * directions[2]
        ) for b in scanner1]
        distances1 = pairwise_distances(rotated)

        overlaps = [k for k, v in distances0.items() if v in distances1.values()]
        overlaps = chain.from_iterable(overlaps)
        print(len(set(overlaps)))

        # I'm doing something right as correctly getting 12 overlaps where I should, but a lot to work out still
