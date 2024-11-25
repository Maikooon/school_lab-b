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

    """
    キューに格納されたRWが自分のサーバのものか、もしくは他のサーバのものなのかを調べる

    """

    def random_walk(self, source_id, count, alpha=0.1):
        source_node = self.nodes[source_id]
        executer = source_node.manager
        end_walk = dict()
        escaped_walk = dict()

        # 指定された回数分だけ実行する
        for i in range(count):
            # もし、確率が一定以上だったら、サーバ１に遷移、それ以外ならサーバ２に遷移
            current_node = source_node
            # 終了確立に達するまで繰り返す
            while True:
                beta = random.random()
                # 終了確率に達した時
                if beta < alpha:
                    print("終了確率を計算します", beta)
                    print(type(current_node.id))
                    end_walk[current_node.id] = end_walk.get(current_node.id, 0) + 1
                    break

                # 終了確立には達していないが、隣のサーバに遷移する時
                # 一定の確立で同一サーバ内で遷移いする確立
                if random.random() < 0.2:
                    # 同一サーバ内のノードに遷移
                    if current_node.id == "0":
                        next_node_id = "1"
                    elif current_node.id == "1":
                        next_node_id = "0"
                    elif current_node.id == "2":
                        next_node_id = "3"
                    elif current_node.id == "3":
                        next_node_id = "2"
                    print(
                        "同一サーバ内のノードに遷移します,current_node.id: ",
                        next_node_id,
                    )
                else:

                    if current_node.id == "0" or current_node.id == "1":
                        next_node_id = "2"
                    elif current_node.id == "2" or current_node.id == "3":
                        next_node_id = "0"
                    escaped_walk[next_node_id] = escaped_walk.get(next_node_id, 0) + 1
                    print("隣のサーバに遷移します、current_node.id: ", next_node_id)
                    break

        return end_walk, escaped_walk
