import os
import numpy as np


# Read in data: List of coords [(6, 10), (0, 14), ...], and list of folds [('y', 7), ('x', 5)...]
with open(os.path.join('data', 'day_13.txt'), 'r') as f:
    coords, folds = f.read().split('\n\n')
    coords = [(int(line.split(',')[0]), int(line.split(',')[1])) for line in coords.split()]
    folds = [(line.split('=')[0][-1], int(line.split('=')[1])) for line in folds.split('\n')]

# Create grid of required dimensions
x_dim = 2 * max(fold[1] for fold in folds if fold[0] == 'x') + 1
y_dim = 2 * max(fold[1] for fold in folds if fold[0] == 'y') + 1
x_coords, y_coords = zip(*coords)
grid = np.zeros((y_dim, x_dim), dtype=bool)
grid[y_coords, x_coords] = 1


def fold(grid, axis, position):
    if axis == 'y':
        top = grid[:position]
        bottom = np.flip(grid[position+1:], axis=0)
        new_grid = top | bottom
    else:
        left = grid[:, :position]
        right = np.flip(grid[:, position+1:], axis=1)
        new_grid = left | right
    return new_grid


# Part 1 - first fold only
axis, position = folds[0]
completed_grid = fold(grid, axis, position)
print(f'Part 1 Solution: {completed_grid.sum()}')


# Part 2 - all folds
for axis, position in folds:
    grid = fold(grid, axis, position)

# Can just about make out the eight letters by printing them this way
for i in range(0, grid.shape[1], grid.shape[1] // 8):
    letter = np.where(grid[:, i: i + grid.shape[1] // 8 - 1], '#', '.')
    print(letter, end='\n\n')

# My solution was HKUJGAJZ:
# [['#' '.' '.' '#']
#  ['#' '.' '.' '#']
#  ['#' '#' '#' '#']
#  ['#' '.' '.' '#']
#  ['#' '.' '.' '#']
#  ['#' '.' '.' '#']]

# [['#' '.' '.' '#']
#  ['#' '.' '#' '.']
#  ['#' '#' '.' '.']
#  ['#' '.' '#' '.']
#  ['#' '.' '#' '.']
#  ['#' '.' '.' '#']]

# [['#' '.' '.' '#']
#  ['#' '.' '.' '#']
#  ['#' '.' '.' '#']
#  ['#' '.' '.' '#']
#  ['#' '.' '.' '#']
#  ['.' '#' '#' '.']]

# [['.' '.' '#' '#']
#  ['.' '.' '.' '#']
#  ['.' '.' '.' '#']
#  ['.' '.' '.' '#']
#  ['#' '.' '.' '#']
#  ['.' '#' '#' '.']]

# [['.' '#' '#' '.']
#  ['#' '.' '.' '#']
#  ['#' '.' '.' '.']
#  ['#' '.' '#' '#']
#  ['#' '.' '.' '#']
#  ['.' '#' '#' '#']]

# [['.' '#' '#' '.']
#  ['#' '.' '.' '#']
#  ['#' '.' '.' '#']
#  ['#' '#' '#' '#']
#  ['#' '.' '.' '#']
#  ['#' '.' '.' '#']]

# [['.' '.' '#' '#']
#  ['.' '.' '.' '#']
#  ['.' '.' '.' '#']
#  ['.' '.' '.' '#']
#  ['#' '.' '.' '#']
#  ['.' '#' '#' '.']]

# [['#' '#' '#' '#']
#  ['.' '.' '.' '#']
#  ['.' '.' '#' '.']
#  ['.' '#' '.' '.']
#  ['#' '.' '.' '.']
#  ['#' '#' '#' '#']]
