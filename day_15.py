# Probably not the intended solution as part 2 took an hour to run, but it worked.

import os
import numpy as np
from queue import PriorityQueue
from collections import defaultdict


# Graph class and Dijkstra's algorithm function taken from:
# https://stackabuse.com/dijkstras-algorithm-in-python/
# Adapted as follows:
#  - Used dicts rather than lists to only store necessary edges rather than lots of -1s to denote unconnected vertices.
#  - Set a weight for each direction rather than same weight in each direction.


class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = defaultdict(dict)
        self.visited = []

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight


def dijkstra(graph, start_vertex):
    d = {v: float('inf') for v in range(graph.v)}
    d[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in graph.edges[current_vertex]:
            distance = graph.edges[current_vertex][neighbor]
            if neighbor not in graph.visited:
                old_cost = d[neighbor]
                new_cost = d[current_vertex] + distance
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    d[neighbor] = new_cost
    return d


def construct_graph_from_grid(grid):
    y_dim, x_dim = grid.shape
    total_vertices = y_dim * x_dim
    g = Graph(total_vertices)
    for i in range(y_dim):
        for j in range(x_dim):
            this_node_idx = i * x_dim + j
            if i < y_dim - 1:
                vertical_neighbour_idx = (i + 1) * x_dim + j
                vertical_neighbour_val = grid[i + 1, j]
                g.add_edge(this_node_idx, vertical_neighbour_idx, vertical_neighbour_val)
            if j < x_dim - 1:
                horizontal_neighbour_idx = i * x_dim + j + 1
                horizontal_neighbour_val = grid[i, j + 1]
                g.add_edge(this_node_idx, horizontal_neighbour_idx, horizontal_neighbour_val)
            if i > 0:
                vertical_neighbour_idx = (i - 1) * x_dim + j
                vertical_neighbour_val = grid[i - 1, j]
                g.add_edge(this_node_idx, vertical_neighbour_idx, vertical_neighbour_val)
            if j > 0:
                horizontal_neighbour_idx = i * x_dim + j - 1
                horizontal_neighbour_val = grid[i, j - 1]
                g.add_edge(this_node_idx, horizontal_neighbour_idx, horizontal_neighbour_val)
    return g


def get_data():
    with open(os.path.join('data', 'day_15.txt'), 'r') as f:
        return np.array([list(line.strip()) for line in f.readlines()], dtype=int)


# Part 1
data = get_data()
g = construct_graph_from_grid(data)
shortest_distance = dijkstra(g, 0)[g.v-1]
print(f'Part 1 Solution: {shortest_distance}')


# Part 2
small = get_data()
num_repeats = 5
y_dim_small, x_dim_small = small.shape
y_dim = y_dim_small * num_repeats
x_dim = x_dim_small * num_repeats
data = np.zeros(shape=(y_dim, x_dim), dtype=int)

for i in range(num_repeats):
    for j in range(num_repeats):
        y_start = i * y_dim_small
        y_end = y_start + y_dim_small
        x_start = j * x_dim_small
        x_end = x_start + x_dim_small
        grid = small.copy()
        iterations = i + j
        for _ in range(iterations):
            grid = np.where(grid == 9, 1, grid + 1)
        data[y_start:y_end, x_start:x_end] = grid


g = construct_graph_from_grid(data)
shortest_distance = dijkstra(g, 0)[g.v-1]
print(f'Part 2 Solution: {shortest_distance}')
