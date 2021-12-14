import os
import re
from collections import Counter
from functools import cache


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


# Part 2 - 40 iterations is too many to build string, need to recursively count insertions instead
@cache
def get_counts(pair, n=0):
    """For a pair of letters, return the character counts after 40 iterations of growth."""
    if n == 40:
        return Counter()
    insertion = insertions[pair]
    new_pair_1 = pair[0] + insertion
    new_pair_2 = insertion + pair[1]
    return Counter(insertion) + get_counts(new_pair_1, n+1) + get_counts(new_pair_2, n+1)


polymer = template
pairs = [polymer[i:i+2] for i in range(len(polymer)-1)]
counter = Counter(polymer)
for pair in pairs:
    counter += get_counts(pair)
solution = max(counter.values()) - min(counter.values())
print(f'Part 2 Solution: {solution}')
