import os
import numpy as np
import pandas as pd


# Get data
with open(os.path.join('data', 'day_01.txt'), 'r') as f:
    data = [int(line) for line in f.readlines()]

# Part 1
depths = np.array(data)
diffs = depths - np.roll(depths, 1)
solution = (diffs > 0).sum()
print(f'Part 1 Solution: {solution}')

# Part 2
windows = pd.Series(depths).rolling(window=3).sum()
diffs = windows - np.roll(windows, 1)
solution = (diffs > 0).sum()
print(f'Part 2 Solution: {solution}')
