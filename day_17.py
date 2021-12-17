import os
import re
from itertools import product
from typing import Optional


# Read data from file and extract the four required values
with open(os.path.join('data', 'day_17.txt'), 'r') as f:
    string = f.read().strip()
pattern = r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)'
x1, x2, y1, y2 = map(int, re.match(pattern, string).groups())


def launch(xv: int, yv: int) -> Optional[int]:
    """Return highest point reached if successful, return None if unsuccessful."""
    x, y = 0, 0
    highest = 0
    while x <= x2 and y >= y1:
        x += xv
        y += yv
        xv = 0 if xv <= 1 else xv - 1
        yv -= 1
        if y > highest:
            highest = y
        if (x1 <= x <= x2) and (y2 >= y >= y1):
            return highest


# Probably searching a much larger range of velocities than necessary but still runs quickly
velocities = product(range(-max(abs(x2), abs(y1))-1, max(abs(x2), abs(y1))+1), repeat=2)
results = {}
for velocity in velocities:
    result = launch(*velocity)
    if result is not None:
        results[velocity] = result
print(f'Part 1 Solution: {max(results.values())}')
print(f'Part 2 Solution: {len(results.values())}')
