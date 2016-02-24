import locale
import random
import time

import numpy as np
import matplotlib.pyplot as plt

from graph import *
from sets import Set

class DepthFirstGenerator:
    def __init__(self, graph, start_vertex):
        self.graph = graph
        self.stack = [start_vertex]
        self.visited_vertex = Set([start_vertex])

    def next_step(self):
        while self.stack != []:
            v1 = self.stack[-1]

            neighbors = []
            for edge in self.graph.incident_edges(v1):
                v2 = edge.opposite(v1)
                if not v2 in self.visited_vertex:
                    neighbors.append(v2)

            if neighbors == []:
                self.stack.pop()
            else:
                random.shuffle(neighbors)
                v2 = neighbors[0]
                self.visited_vertex.add(v2)
                self.stack.append(v2)
                edge = graph.get_edge(v1, v2)
                edge.element().set_open();
                break

    def is_over(self):
        return self.stack == []

class Wall:
    def __init__(self):
        self._is_closed = True

    def is_closed(self):
        return self._is_closed

    def set_open(self):
        self._is_closed = False

class Cell:
    def __init__(self, coordinate):
        self._coordinate = coordinate

    def get_coordinate(self):
        return self._coordinate

size = (32, 64)

graph = Graph()

maze = [[graph.insert_vertex(Cell((y, x))) for x in range(size[1])] \
        for y in range(size[0])]

start_vertex = maze[0][0]
end_vertex = maze[-1][-1]

# Add vertical edges
for y in range(size[0]-1):
    for x in range(size[1]):
        graph.insert_edge(maze[y][x], maze[y+1][x], Wall())

# Add horizontal edges
for y in range(size[0]):
    for x in range(size[1]-1):
        graph.insert_edge(maze[y][x], maze[y][x+1], Wall())

generator = DepthFirstGenerator(graph, start_vertex)
while not generator.is_over():
    generator.next_step()

# Graphic representation with matplotlib
maze_figure = np.zeros((size[0]*2+1, size[1]*2+1), dtype=float)

for edge in graph.edges():
    if not edge.element().is_closed():
        u, v = edge.endpoints()
        u_coord = u.element().get_coordinate()
        v_coord = v.element().get_coordinate()
        edge_y = 2*u_coord[0]+1 + v_coord[0] - u_coord[0]
        edge_x = 2*u_coord[1]+1 + v_coord[1] - u_coord[1]
        maze_figure[edge_y][edge_x] = 1

for vertex in graph.vertices():
    y, x = vertex.element().get_coordinate();
    y = 2*y+1
    x = 2*x+1
    maze_figure[y][x] = 1

maze_figure[1][0] = 1
maze_figure[-2][-1] = 1

plt.figure(figsize=(2*9,9))
plt.subplot(111,frameon=False)
plt.imshow(maze_figure,
        interpolation='nearest',
        cmap=plt.cm.hot, vmin=0,
        vmax=1)
plt.xticks([]), plt.yticks([])
plt.show()


