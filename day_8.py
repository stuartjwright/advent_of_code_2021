import os
from collections import Counter

with open(os.path.join('data', 'day_8.txt'), 'r') as f:
    data = [line.strip().split('|') for line in f.readlines()]


# Part 1
targets = [2, 3, 4, 7]
outputs = [line[-1].strip().split() for line in data]
counts = [len([signal for signal in line if len(signal) in targets]) for line in outputs]
print(f'Part 1 Solution: {sum(counts)}')


# Part 2

# Some lookups we'll need
num_segments_map = {
    0: ['a', 'b', 'c', 'e', 'f', 'g'],
    1: ['c', 'f'],
    2: ['a', 'c', 'd', 'e', 'g'],
    3: ['a', 'c', 'd', 'f', 'g'],
    4: ['b', 'c', 'd', 'f'],
    5: ['a', 'b', 'd', 'f', 'g'],
    6: ['a', 'b', 'd', 'e', 'f', 'g'],
    7: ['a', 'c', 'f'],
    8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9: ['a', 'b', 'c', 'd', 'f', 'g']
}
segments_num_map = {''.join(v): k for k, v in num_segments_map.items()}
unique_counts = {2: 1, 3: 7, 4: 4, 7: 8}

total = 0
for signals, outputs in data:

    signals = signals.strip().split()
    outputs = outputs.strip().split()

    known_segments = {}
    known_signals = {}

    # Start with the easy ones (1, 4, 7, 8) that can be deduced from their unique lengths
    for signal in signals:
        if (n := len(signal)) in unique_counts:
            known_signals[unique_counts[n]] = signal

    # Whichever segment is in 7 but not 1 is segment a
    a = ''.join(set(known_signals[7]) - set(known_signals[1]))
    known_segments['a'] = a

    # Of the two segments in 1, c must be in 8 different nums, whereas f is in 9
    segment_counter = Counter(''.join(signals))
    segments = known_signals[1]
    c, f = sorted(segments, key=lambda s: segment_counter[s])
    known_segments['c'] = c
    known_segments['f'] = f

    # Of the other two segments in 4 (b & d), we can work out which way around from their frequencies (6 & 7)
    segments = ''.join(c for c in known_signals[4] if c not in known_segments.values())
    b, d = sorted(segments, key=lambda s: segment_counter[s])
    known_segments['b'] = b
    known_segments['d'] = d

    # We can then work out e (which appears 4 times) and g (7 times). All segments now known.
    inverse_counter = {v: k for k, v in segment_counter.items() if k not in known_segments.values()}
    known_segments['e'] = inverse_counter[4]
    known_segments['g'] = inverse_counter[7]

    # Now we can use the segment map to decode the full signal patterns
    known_segments_inverse = {v: k for k, v in known_segments.items()}
    decoded = {}
    for signal in signals:
        decoded[''.join(sorted(signal))] = segments_num_map[''.join(sorted(known_segments_inverse[c] for c in signal))]

    # Finally, use the decoded map we just created to decode the outputs
    digits = []
    for output in outputs:
        digits.append(decoded[''.join(sorted(output))])
    result = int(''.join(str(d) for d in digits))
    total += result
print(f'Part 2 Solution: {total}')
