from Node import *
import random
from queue import Queue


class Graph:
    def __init__(self, ADJ, nodes):
        self.nodes = dict()
        self.outside_nodes = dict()
        self.all_nodes = dict()

        for node_id in ADJ.keys():
            self.nodes[node_id] = nodes[node_id]
            self.all_nodes[node_id] = nodes[node_id]
            for adjacent_id in ADJ[node_id]:
                self.nodes[node_id].add_edge(nodes[adjacent_id])
                if adjacent_id not in ADJ.keys():
                    self.outside_nodes[adjacent_id] = self.nodes[node_id].adj[
                        adjacent_id
                    ]
                    self.all_nodes[adjacent_id] = nodes[adjacent_id]

        self.node_count = len(self.nodes)

    def __repr__(self):
        adj = dict()
        for node in self.nodes.values():
            adj[str(node)] = set()
            for adj_node in node.adj:
                adj[str(node)].add(str(adj_node))
        return str(adj)

    def random_walk(self, source_id, count, alpha=0.15):
        source_node = self.nodes[source_id]
        executer = source_node.manager
        end_walk = dict()
        escaped_walk = dict()

        for i in range(count):
            current_node = source_node
            while True:
                print("Random Walk    ここの数がHop数")
                if current_node.manager != executer:
                    print("他のサーバに遷移しす,node_id: ", current_node.id)
                    # 次にどこから始まるのか記録しておく部分
                    escaped_walk[current_node.id] = (
                        escaped_walk.get(current_node.id, 0) + 1
                    )
                    print(escaped_walk)
                    # グラフではないときも、ここで調整可能にする
                    break
                if random.random() < alpha:
                    # ここに入っているのはただの数字
                    print("終了確立に達しました,node_id: ", current_node.id)
                    end_walk[current_node.id] = end_walk.get(current_node.id, 0) + 1
                    break
                current_node = current_node.get_random_adjacent()
                print("次のノード", current_node.id)

        return end_walk, escaped_walk
