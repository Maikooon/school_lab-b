from Node import *
import random
from queue import Queue
import time


class Graph:
    def __init__(self, ADJ, nodes, ng_list):
        print("初期化しました")
        self.nodes = dict()
        self.outside_nodes = dict()
        self.all_nodes = dict()
        self.all_paths = []
        self.ng_list = ng_list
        self.total_determinate_ng_nodes = 0

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

    def determine_next_hop(self, next_node_id, start_node_id):
        """
        次ノードへのホップを許可するかどうかを判定する関数。

        Parameters:
            source_community: 現在のノードが属するコミュニティID。
            next_node_id: 次に移動しようとしているノードのID。

        Returns:
            bool: True ならホップ許可、False ならホップ不可。
        """

        ng_lists = self.ng_list
        # print(f"NGリスト: {ng_lists}")
        # TODO;ここが含まれていると莫大に時間が増えてしまう
        print(type(next_node_id))  # int
        # next_node_id = 199
        # next_node_IdがNGリストに含まれているかどうかを確認
        if next_node_id in ng_lists:
            print(f"次ノード {next_node_id} は出発先によってはNGです")
            print(f"出発ノード {start_node_id} が含まれているか確認")  # int
            start_node_id = int(start_node_id)
            print(type(start_node_id))  # int
            # print(f"199のNGリスト: {ng_lists[next_node_id]}")
            if start_node_id in ng_lists[next_node_id]:
                # If both conditions are met, return False (hop not allowed)
                # return False
                print(f"次ノード {next_node_id} へのホップはNGです。")

        # 　含まれていたら、その左の配列に、Start＿nodeが含まれているのか確認
        return True

    def random_walk(
        self,
        source_id,
        count,
        alpha=0.2,
        all_paths=None,
        start_node_id=None,
        start_node_community=None,
    ):
        # print("random_walkの関数が開始")
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
                # 現在のノードが異なるサーバかチェック
                if current_node.manager != executer:
                    # 権限がある場合、異なるサーバに移動
                    escaped_walk[current_node.id] = (
                        escaped_walk.get(current_node.id, 0) + 1
                    )
                    break  # サーバ移動を記録してループを終了

                # 終了確率より小さいときには終了
                if random.random() < alpha:
                    end_walk[current_node.id] = end_walk.get(current_node.id, 0) + 1
                    self.all_paths.append(current_node.id)
                    # print("RWが終了しました")
                    break

                # TODO:kここで認可を行うーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
                start_time_determinate = time.time()  # 時間を計測
                # source_community = self.node_community_mapping.get(start_node_id)
                if not self.determine_next_hop(int(current_node.id), start_node_id):
                    print(
                        f"RWが一番初めにスタートしたComは{start_node_community}です。Roleを確認したところノード {current_node.id} へのホップはNGです。次のノードを選びます。"
                    )
                    continue  # NGの場合、次のノードに移動しないで再度選択
                end_time_determinate = time.time()  # 時間を計測
                elapsed_time_determinate = end_time_determinate - start_time_determinate
                self.total_determinate_ng_nodes += elapsed_time_determinate
                # TODO:ここまで----------------------------------------------------------------------------------

                # 通ったノードを追加する
                self.all_paths.append(current_node.id)

                # 最後に次のノードを選択
                next_node = current_node.get_random_adjacent()

                # 次のノードを現在のノードに設定
                current_node = next_node

            print("end_walk", end_walk)
            print("escaped_walk", escaped_walk)
            # print("all-paths", self.all_paths)
            print("total_determinate_ng_nodes", self.total_determinate_ng_nodes)

        return end_walk, escaped_walk, self.all_paths
