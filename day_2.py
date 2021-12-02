import os


# Prepare data to get list of instructions in dictionary form, e.g. {'direction': 'forward', 'value': 5}
with open(os.path.join('data', 'day_2.txt'), 'r') as f:
    data = [line.strip().split() for line in f.readlines()]
instructions = [{'direction': line[0], 'value': int(line[1])} for line in data]


# Part 1
def move_forward(position, value):
    position['horizontal'] += value


def move_down(position, value):
    position['depth'] += value


def move_up(position, value):
    position['depth'] -= value


move_functions = {
    'forward': move_forward,
    'down': move_down,
    'up': move_up
}

position = {'horizontal': 0, 'depth': 0}
for instruction in instructions:
    move_submarine = move_functions[instruction['direction']]
    move_submarine(position, instruction['value'])

solution = position['horizontal'] * position['depth']
print(f'Part 1 Solution: {solution}')


# Part 2
def move_forward(position, value):
    position['horizontal'] += value
    position['depth'] += value * position['aim']


def move_down(position, value):
    position['aim'] += value


def move_up(position, value):
    position['aim'] -= value


move_functions = {
    'forward': move_forward,
    'down': move_down,
    'up': move_up
}

position = {'horizontal': 0, 'depth': 0, 'aim': 0}
for instruction in instructions:
    move_submarine = move_functions[instruction['direction']]
    move_submarine(position, instruction['value'])

solution = position['horizontal'] * position['depth']
print(f'Part 2 Solution: {solution}')
