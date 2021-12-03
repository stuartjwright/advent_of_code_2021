import os
import numpy as np


# Get data in 2-d numpy array of 0s and 1s
with open(os.path.join('data', 'day_3.txt'), 'r') as f:
    grid = np.array([list(line.strip()) for line in f.readlines()], dtype=int)
num_codes, num_bits = grid.shape


# Part 1
gamma = int(''.join(str(bit) for bit in (grid.sum(axis=0) > num_codes // 2).astype(int)), base=2)
epsilon = gamma ^ int('1' * num_bits, base=2)
solution = gamma * epsilon
print(f'Part 1 Solution: {solution}')


# Part 2
oxygen = grid.copy()
for i in range(num_bits):
    oxygen = oxygen[oxygen[:, i] == (oxygen[:, i].sum() >= oxygen.shape[0] / 2)]
    if oxygen.shape[0] <= 1:
        break

co2 = grid.copy()
for i in range(num_bits):
    co2 = co2[co2[:, i] == (co2[:, i].sum() < co2.shape[0] / 2)]
    if co2.shape[0] <= 1:
        break

oxygen = int(''.join(str(bit) for bit in oxygen.flatten()), base=2)
co2 = int(''.join(str(bit) for bit in co2.flatten()), base=2)
solution = oxygen * co2
print(f'Part 2 Solution: {solution}')
