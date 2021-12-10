import os
from functools import cache
from typing import Callable


def get_data(path: str, filename: str) -> list[int]:
    """Reads a text file containing comma-separated integers, and returns a
    list of integers. Each integer represents one crab and its initial horizontal position.

    :param path: directory containing data file.
    :param filename: filename of data file.
    :return: list of ints representing starting positions of crabs.
    """
    with open(os.path.join(path, filename), 'r') as f:
        return [int(num) for num in f.read().split(',')]


def find_solution(crabs: list[int], fuel_func: Callable[[int], int]) -> int:
    """Finds the optimal horizontal position which all crabs can reach expending
    the minimum possible fuel.

    :param crabs: list of ints representing initial crab position.
    :param fuel_func: function for calculating fuel expenditure for each crab movement.
    :return: the amount of fuel used in the optimal solution.
    """
    results = {}
    for target in range(max(crabs)):
        fuel = 0
        for crab in crabs:
            steps = abs(target - crab)
            fuel += fuel_func(steps)
        results[target] = fuel
    return min(results.values())


def get_part_1_fuel(steps: int) -> int:
    """Identity function.

    :param steps: number of steps taken by crab.
    :return: the amount of fuel spent (the same as the number of steps for part 1).
    """
    return steps


@cache
def get_part_2_fuel(steps: int) -> int:
    """Calculates fuel expenditure for part 2, where each step by a crab
    costs 1 more fuel than the previous. For example, if a crab is 3 steps away, they spend
    1+2+3=6 fuel. Multiple calls with the same argument will be made, so @cache decorator is
    used to store results for future use, resulting in a significant speed improvement.

    :param steps: number of steps taken by crab.
    :return: the amount of fuel spent by the crab.
    """
    return sum(range(1, steps + 1))


if __name__ == '__main__':
    crabs = get_data('data', 'day_07.txt')
    print(f'Part 1 Solution: {find_solution(crabs, get_part_1_fuel)}')
    print(f'Part 2 Solution: {find_solution(crabs, get_part_2_fuel)}')
