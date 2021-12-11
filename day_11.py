import os
import numpy as np
from itertools import product


def get_data():
    with open(os.path.join('data', 'day_11.txt'), 'r') as f:
        return np.array([list(line.strip()) for line in f.readlines()], dtype=int)


# Part 1
energy = get_data()
flash_count = 0
for _ in range(100):
    energy += 1
    padded = np.pad(energy, pad_width=1, constant_values=0)
    new_flashes = (padded > 9)
    flashes = new_flashes.copy()
    while new_flashes.sum() != 0:
        directions = [direction for direction in product([-1, 0, 1], repeat=2) if direction != (0, 0)]
        flash_neighbours = np.zeros(shape=flashes.shape, dtype=int)
        for direction in directions:
            flash_neighbours += np.roll(new_flashes, shift=direction, axis=(0, 1))
        padded += flash_neighbours
        padded = np.pad(padded[1:-1, 1:-1], pad_width=1, constant_values=0)
        new_flashes = (padded > 9) & ~flashes
        flashes += new_flashes
    padded[flashes] = 0
    energy = padded[1:-1, 1:-1]
    flash_count += flashes.sum()
print(f'Part 1 Solution: {flash_count}')


# Part 2
energy = get_data()
num_steps = 0
while True:
    num_steps += 1
    energy += 1
    padded = np.pad(energy, pad_width=1, constant_values=0)
    new_flashes = (padded > 9)
    flashes = new_flashes.copy()
    while new_flashes.sum() != 0:
        directions = [direction for direction in product([-1, 0, 1], repeat=2) if direction != (0, 0)]
        flash_neighbours = np.zeros(shape=flashes.shape, dtype=int)
        for direction in directions:
            flash_neighbours += np.roll(new_flashes, shift=direction, axis=(0, 1))
        padded += flash_neighbours
        padded = np.pad(padded[1:-1, 1:-1], pad_width=1, constant_values=0)
        new_flashes = (padded > 9) & ~flashes
        flashes += new_flashes
    padded[flashes] = 0
    energy = padded[1:-1, 1:-1]
    if energy.sum() == 0:
        break
print(f'Part 2 Solution: {num_steps}')
