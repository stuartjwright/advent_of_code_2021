import os
import json
import math
from abc import ABC
from itertools import permutations


with open(os.path.join('data', 'day_18.txt'), 'r') as f:
    pairs = [json.loads(line) for line in f.readlines()]


class Element(ABC):
    def reduce(self):
        pass

    def find_pair_to_explode(self):
        return False

    def find_pair_to_split(self):
        return False

    def explode(self):
        pass


class Value(Element):
    def __init__(self, data, parent=None, depth=0):
        self.value = data
        self.parent = parent
        self.depth = depth

    def reconstruct(self):
        return self.value

    def find_pair_to_split(self):
        if self.value >= 10:
            self.parent.replace_split_child(value=self.value, to_replace=self)
            return True

    def increase_depths(self):
        self.depth += 1


class Pair(Element):
    def __init__(self, data, parent=None, depth=0):
        if data is None:
            return
        if len(data) != 2:
            raise ValueError('Error creating pair.')
        if isinstance(left := data[0], int):
            self.left = Value(left, parent=self, depth=depth+1)
        else:
            self.left = Pair(left, parent=self, depth=depth+1)
        if isinstance(right := data[1], int):
            self.right = Value(right, parent=self, depth=depth+1)
        else:
            self.right = Pair(right, parent=self, depth=depth+1)
        self.depth = depth
        self.parent = parent

    def reduce(self):
        while True:
            explode_success = self.find_pair_to_explode()
            if explode_success:
                continue
            split_success = self.find_pair_to_split()
            if not (explode_success or split_success):
                break

    def explode(self):
        self.explode_left(self.left.value)
        self.explode_right(self.right.value)
        self.parent.replace_exploded_child(self)

    def explode_left(self, value):
        left = self.get_left_sibling()
        if left:
            if isinstance(left, Value):
                left.value += value
            elif left is not self:
                left.explode_rightmost_in_left_sibling(value)

    def explode_right(self, value):
        right = self.get_right_sibling()
        if right:
            if isinstance(right, Value):
                right.value += value
            elif right is not self:
                right.explode_leftmost_in_right_sibling(value)

    def get_right_sibling(self):
        parent = self.parent
        if parent is None:
            return
        right = parent.right
        if right is self:
            return parent.get_right_sibling()
        return right

    def get_left_sibling(self):
        parent = self.parent
        if parent is None:
            return
        left = parent.left
        if left is self:
            return parent.get_left_sibling()
        return left

    def explode_leftmost_in_right_sibling(self, value):
        left = self.left
        if isinstance(left, Value):
            left.value += value
        else:
            left.explode_leftmost_in_right_sibling(value)

    def explode_rightmost_in_left_sibling(self, value):
        right = self.right
        if isinstance(right, Value):
            right.value += value
        else:
            right.explode_rightmost_in_left_sibling(value)

    def replace_exploded_child(self, to_replace):
        if self.left is to_replace:
            self.left = Value(0, parent=self, depth=self.depth+1)
        elif self.right is to_replace:
            self.right = Value(0, parent=self, depth=self.depth+1)

    def find_pair_to_explode(self):
        if self.depth == 4:
            self.explode()
            return True
        else:
            if self.left.find_pair_to_explode():
                return True
            return self.right.find_pair_to_explode()

    def reconstruct(self):
        left = self.left.reconstruct()
        right = self.right.reconstruct()
        return [left, right]

    def find_pair_to_split(self):
        if self.left.find_pair_to_split():
            return True
        return self.right.find_pair_to_split()

    def replace_split_child(self, value, to_replace):
        half = value / 2
        left = math.floor(half)
        right = math.ceil(half)
        new_pair = Pair([left, right], parent=self, depth=self.depth+1)
        if self.left is to_replace:
            self.left = new_pair
        else:
            self.right = new_pair

    def add(self, right):
        parent = Pair(data=None)
        right_pair = Pair(right, parent=parent, depth=self.depth)
        right_pair.increase_depths()
        self.increase_depths()
        self.parent = parent
        parent.left = self
        parent.right = right_pair
        parent.depth = self.depth - 1
        parent.parent = None
        return parent

    def increase_depths(self):
        self.depth += 1
        self.left.increase_depths()
        self.right.increase_depths()

    def get_magnitude_left(self):
        left = self.left
        if isinstance(left, Value):
            return left.value
        return left.get_magnitude()

    def get_magnitude_right(self):
        right = self.right
        if isinstance(right, Value):
            return right.value
        return right.get_magnitude()

    def get_magnitude(self):
        return 3 * self.get_magnitude_left() + 2 * self.get_magnitude_right()


if __name__ == '__main__':
    # Part 1
    current = Pair(pairs[0])
    for pair in pairs[1:]:
        current = current.add(pair)
        current.reduce()
    print(f'Part 1 Solution: {current.get_magnitude()}')

    # Part 2
    perms = permutations(pairs, 2)
    largest = 0
    for x, y in perms:
        combined = Pair(x).add(y)
        combined.reduce()
        magnitude = combined.get_magnitude()
        if magnitude > largest:
            largest = magnitude
    print(f'Part 2 Solution: {largest}')
