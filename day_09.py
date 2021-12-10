import os
import numpy as np
from itertools import product


# Data is a 2d-grid of single-digit ints, read them into 2d numpy array
with open(os.path.join('data', 'day_09.txt'), 'r') as f:
    grid = np.array([list(line.strip()) for line in f.readlines()], dtype=int)


# Part 1
# General idea here is that we pad the outer perimeter of the grid with 10s
# This way any low point in the original grid now has exactly 4 higher neighbours
padded = np.pad(grid, pad_width=1, constant_values=10)
total_lower_neighbours = np.zeros(shape=padded.shape)
shifts = (1, -1)
axes = (0, 1)
for shift, axis in product(shifts, axes):
    total_lower_neighbours += padded < np.roll(padded, shift, axis)
unpadded_lower_neighbours = total_lower_neighbours[1:-1, 1:-1]
risk_levels = np.where(unpadded_lower_neighbours == 4, grid + 1, 0)
total_risk = risk_levels.sum()
print(f'Part 1 Solution: {total_risk}')


# Part 2
def add_neighbours(grid, i, j, value):
    """Recursively add neighbours to basin in all directions until hitting a lower value
    or a value >= 9. The basin variable is a set defined outside the function.
    """
    if value >= 9:
        return
    basin.add((i, j))
    if (new_value := grid[i+1, j]) > value:
        add_neighbours(grid, i+1, j, new_value)
    if (new_value := grid[i, j+1]) > value:
        add_neighbours(grid, i, j+1, new_value)
    if (new_value := grid[i-1, j]) > value:
        add_neighbours(grid, i-1, j, new_value)
    if (new_value := grid[i, j-1]) > value:
        add_neighbours(grid, i, j-1, new_value)


low_point_indices = np.argwhere(total_lower_neighbours == 4)
basins = []
for i, j in low_point_indices:
    basin = set()
    add_neighbours(padded, i, j, padded[i, j])
    basins.append(len(basin))

size_3, size_2, size_1 = sorted(basins)[-3:]
solution = size_1 * size_2 * size_3
print(f'Part 2 Solution: {solution}')
