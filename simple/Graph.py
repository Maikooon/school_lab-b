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

    def random_walk(self, source_id, count, alpha=0.05):
        source_node = self.nodes[source_id]
        executer = source_node.manager
        end_walk = dict()
        escaped_walk = dict()

        # 指定された回数分だけ実行する
        for i in range(count):
            # もし、確率が一定以上だったら、サーバ１に遷移、それ以外ならサーバ２に遷移
            current_node = source_node
            print("ここへの到達をかくにん")
            # 終了確立に達するまで繰り返す
            while True:
                print("Random Walk    ここの数がHop数")
                # 終了確立には達していないが、隣のサーバに遷移する時
                if current_node.manager != executer:
                    # 隣接のだけ指定してそのまm移行できるようにしたい
                    escaped_walk[current_node.id] = (
                        escaped_walk.get(current_node.id, 0) + 1
                    )
                    print(escaped_walk)
                    break
                print("確率を計算します", alpha)
                beta = random.random()

                # 終了確率に達した時
                if beta < alpha:
                    print("終了確率を計算します", beta)
                    # end_walk[current_node.id] = end_walk.get(current_node.id, 0) + 1
                    break

                # 終了確立はクリア、同じサーバ内で遷移する時には適当に隣接ノードを選択
                # current_node = current_node.get_random_adjacent()
                print("終了確立には達しなかったので、そのまま遷移を続けます")
                # print("次のノード", current_node.id)

        return end_walk, escaped_walk
