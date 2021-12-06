import os
from collections import Counter


# Get data - list of ints where each int represents a fish and its internal timer
def get_data():
    with open(os.path.join('data', 'day_6.txt'), 'r') as f:
        return [int(num) for num in f.read().strip().split(',')]


# Some constants we need for both parts
reset_timer = 6
new_fish_timer = 8
reset_threshold = 0


# Part 1 - simulate 80 days
fishes = get_data()
days = 80
for _ in range(days):
    new_fishes = []
    for i, fish in enumerate(fishes):
        if fish == reset_threshold:
            new_fishes.append(new_fish_timer)
            fishes[i] = reset_timer
        else:
            fishes[i] = fish - 1
    fishes.extend(new_fishes)
print(f'Part 1 Solution: {len(fishes)}')


# Part 2 - simulate 256 days
# List will grow too large if we store each datapoint individually so use a dict to summarise instead
days = 256
fishes = get_data()
counter = Counter(fishes)
for _ in range(days):
    new_counter = {}
    for timer, count in reversed(sorted(counter.items())):
        if timer == reset_threshold:
            new_counter[new_fish_timer] = count
            new_counter[reset_timer] = new_counter.get(reset_timer, 0) + count
        else:
            new_counter[timer-1] = count
    counter = new_counter
print(f'Part 2 Solution: {sum(counter.values())}')
