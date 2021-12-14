import os
import re
from collections import Counter


with open(os.path.join('data', 'day_14.txt'), 'r') as f:
    template, insertions = f.read().strip().split('\n\n')
    insertions = dict([insertion.split(' -> ') for insertion in insertions.split('\n')])


def replace(match):
    """Function passed to re.sub to make the appropriate replacement."""
    start, end = match.span()
    group = polymer[start: end+1]
    insertion = insertions[group]
    replacement = match.group(0) + insertion
    return replacement


# Part 1 can just be brute forced with regex
# Find matches using pattern with lookaheads to make sure overlapping matches are handled correctly
pattern = '|'.join(k[0] + '(?=' + k[1] + ')' for k in insertions)
polymer = template
for _ in range(10):
    polymer = re.sub(pattern, replace, polymer)
    counter = Counter(polymer)

counter = Counter(polymer)
solution = max(counter.values()) - min(counter.values())
print(f'Part 1 Solution: {solution}')


# Part 2 - 40 iterations is too many to brute force, need to find some counting algorithm instead
polymer = template

