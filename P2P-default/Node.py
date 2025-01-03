import random

class Node():
    def __init__(self, id, manager=None):
        self.id = id
        self.adj = dict()
        self.degree = 0
        self.manager = manager #IP e.g., 127.0.0.1

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.id == other.id

    def add_edge(self, node):
        self.adj[node.id] = node
        self.degree = len(self.adj)
        # print('Node {} add edge to {}'.format(self.id, node.id))
        return

    def get_random_adjacent(self):
        if self.degree == 0:
            return self
        else:
            return random.choice(list(self.adj.values()))
