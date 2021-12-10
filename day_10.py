import os
import logging


# Change level to 'DEBUG' to see more detailed output
logging.basicConfig(format=f'%(levelname)s: %(message)s', level='INFO')

# Input data is just a list of strings
with open(os.path.join('data', 'day_10.txt'), 'r') as f:
    lines = [line.strip() for line in f.readlines()]

# Some lookups we need for both parts
opens = ['(', '[', '{', '<']
closes = [')', ']', '}', '>']
open_close_map = dict(zip(opens, closes))

# Part 1
score_map = dict(zip(closes, [3, 57, 1197, 25137]))
all_scores = []
for line in lines:
    unclosed = []
    score = 0
    for char in line:
        if char in opens:
            unclosed.append(char)
        elif char == open_close_map[unclosed[-1]]:
            unclosed.pop()
        else:
            score = score_map[char]
            expected = open_close_map[unclosed[-1]]
            logging.debug(f'Corrupted line: {line}. Expected {expected}, but found {char}. Score: {score}.')
            break
    all_scores.append(score)
total_score = sum(all_scores)
logging.info(f'Part 1 Solution: {total_score}')

# Part 2
score_map = dict(zip(closes, range(1, 5)))
incomplete = [line for line, score in zip(lines, all_scores) if score == 0]
all_scores = []
for line in incomplete:
    unclosed = []
    for char in line:
        if char in opens:
            unclosed.append(char)
        else:
            unclosed.pop()
    closers = [open_close_map[char] for char in reversed(unclosed)]
    score = 0
    for closer in closers:
        score *= 5
        score += score_map[closer]
    logging.debug(f'Incomplete line: {line}. Complete by adding {"".join(closers)}. Score: {score}.')
    all_scores.append(score)
middle_score = sorted(all_scores)[len(all_scores) // 2]
logging.info(f'Part 2 Solution: {middle_score}')
