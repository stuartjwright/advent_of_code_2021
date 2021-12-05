import os
import numpy as np


# Get data - list of start coords and list of end coords
with open(os.path.join('data', 'day_5.txt'), 'r') as f:
    coords = [line.strip().split(' -> ') for line in f.readlines()]
starts, ends = zip(*coords)
starts = [tuple(map(int, start.split(','))) for start in starts]
ends = [tuple(map(int, end.split(','))) for end in ends]

# Create numpy array of zeroes large enough to cover all lines
x_dim = max([start[0] for start in starts] + [end[0] for end in ends]) + 1
y_dim = max([start[1] for start in starts] + [end[1] for end in ends]) + 1
grid = np.zeros(shape=(y_dim, x_dim), dtype=int)

# Part 1 solution: add 1 for each cell that falls on a horizontal or vertical lines
for start, end in zip(starts, ends):
    x1, y1 = start
    x2, y2 = end
    if x1 == x2:
        x_range = x1
        min_y, max_y = sorted([y1, y2])
        y_range = np.arange(min_y, max_y+1)
    elif y1 == y2:
        min_x, max_x = sorted([x1, x2])
        y_range = y1
        x_range = np.arange(min_x, max_x+1)
    else:
        continue
    grid[y_range, x_range] += 1
solution = (grid >= 2).sum()
print(f'Part 1 Solution: {solution}')


# Part 2 solution: add diagonal lines to the grid that already has horizontal and verticals
for start, end in zip(starts, ends):
    x1, y1 = start
    x2, y2 = end
    if x1 == x2 or y1 == y2:
        # we already dealt with these in part 1
        continue
    if abs(x1 - x2) == abs(y1 - y2):
        if x1 < x2:
            x_range = np.arange(x1, x2+1)
        else:
            x_range = np.arange(x1, x2-1, -1)
        if y1 < y2:
            y_range = np.arange(y1, y2+1)
        else:
            y_range = np.arange(y1, y2-1, -1)
        grid[y_range, x_range] += 1
solution = (grid >= 2).sum()
print(f'Part 2 Solution: {solution}')
