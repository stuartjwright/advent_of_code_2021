import os
import pandas as pd
import numpy as np
from io import StringIO


# Read in data: a list of ints for drawn numbers, and a 3-d numpy array of all boards
with open(os.path.join('data', 'day_04.txt'), 'r') as f:
    data = f.read().split('\n\n')
    draw, *boards = data
    draw = [int(num) for num in draw.split(',')]
    boards = [pd.read_csv(StringIO(board), sep=r'\s+', header=None) for board in boards]
    boards = pd.concat(boards).to_numpy().reshape(-1, 5, 5)


# Part 1
hits = np.zeros(shape=boards.shape, dtype=int)
for num in draw:
    hits[boards == num] = 1
    col_sums = hits.sum(axis=1)
    row_sums = hits.sum(axis=2)
    all_sums = np.concatenate([col_sums, row_sums], axis=1)
    if (all_sums == 5).any():
        winning_idx, _ = np.argwhere(all_sums == 5)[0]
        winning_board = boards[winning_idx]
        winning_hits = hits[winning_idx]
        solution = np.where(~(winning_hits == 1), winning_board, 0).sum() * num
        print(f'Part 1 Solution: {solution}')
        break


# Part 2
hits = np.zeros(shape=boards.shape, dtype=int)
for num in draw:
    hits[boards == num] = 1
    col_sums = hits.sum(axis=1)
    row_sums = hits.sum(axis=2)
    all_sums = np.concatenate([col_sums, row_sums], axis=1)
    winners = np.argwhere((all_sums == 5).any(axis=1) == 1).flatten()
    if winners.shape[0] == boards.shape[0] - 1:
        last_idx = np.argwhere((all_sums != 5).all(axis=1) == 1).flatten()[0]
    elif winners.shape[0] == boards.shape[0]:
        last_board = boards[last_idx]
        last_hits = hits[last_idx]
        solution = np.where(~(last_hits == 1), last_board, 0).sum() * num
        print(f'Part 2 Solution: {solution}')
        break
