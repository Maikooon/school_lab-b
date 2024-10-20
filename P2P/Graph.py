from Node import *
import random
from queue import Queue


class Graph:
    def __init__(self, ADJ, nodes):
        print("初期化しました")
        self.nodes = dict()
        self.outside_nodes = dict()
        self.all_nodes = dict()
        self.all_paths = []

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

    def random_walk(self, source_id, count, alpha=0.85, all_paths=None):
        print("random_walk-0,2")
        source_node = self.nodes[source_id]
        executer = source_node.manager
        end_walk = dict()
        escaped_walk = dict()

        # Use passed all_paths if available

        if all_paths is None:
            self.all_paths = []
            self.all_paths.append(source_node.id)
        else:
            self.all_paths = all_paths

        # 指定された数だけRWする
        for i in range(count):
            current_node = source_node
            while True:
                # 異なるサーバに移動
                if current_node.manager != executer:
                    escaped_walk[current_node.id] = (
                        escaped_walk.get(current_node.id, 0) + 1
                    )
                    break
                # 終了確率より小さいときには終了
                if random.random() < alpha:
                    end_walk[current_node.id] = end_walk.get(current_node.id, 0) + 1
                    print("RWが終了しました")
                    break
                """
                ここで次のノードの選択をしている
                具体的な選択ノードはNOde.jsに定義されているので、そちらを参照
                
                """
                current_node = current_node.get_random_adjacent()
                # 通ったノードを追加する
                self.all_paths.append(current_node.id)
            print("end_walk", end_walk)
            print("escaped_walk", escaped_walk)
            print("all-paths", self.all_paths)
        return end_walk, escaped_walk, self.all_paths
