from Node import *
import random
from queue import Queue
import time
import os

LOG_FILE_PATH = "./access_limit_time.txt"  # 保存先のログファイルパス


def save_notify_log(user, end_walk, total_determinate_ng_node):
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(f"Notified to {user}, End Walk: {end_walk}\n")
        log_file.write(f"total_determinate_ng_nodes: {total_determinate_ng_node}\n")
        log_file.write("-" * 40 + "\n")


class Graph:
    def __init__(self, ADJ, nodes, node_community_mapping, community_groups, ng_list):
        print("初期化しました")
        self.nodes = dict()
        self.outside_nodes = dict()
        self.all_nodes = dict()
        self.all_paths = []
        self.node_community_mapping = node_community_mapping
        self.community_groups = community_groups
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

    def determine_next_hop(self, source_community, next_node_id, start_node_community):
        """
        次ノードへのホップを許可するかどうかを判定する関数。

        Parameters:
            source_community: 現在のノードが属するコミュニティID。
            next_node_id: 次に移動しようとしているノードのID。

        Returns:
            bool: True ならホップ許可、False ならホップ不可。
        """

        # 次ノードのコミュニティIDを取得
        next_community = self.node_community_mapping.get(next_node_id)
        # start_noce_communityがNoneの場合は、初めのノードとして扱う
        print(f"次ノード {next_node_id} のコミュニティID: {next_community}")
        print(f"始点コミュニティID: {start_node_community}")

        # 始点コミュニティとHopする先が同じであるとき,始点コミュニティには許可なくアクセス可能
        if start_node_community == next_community:
            print(
                f"始点コミュニティ {start_node_community} と次ノード {next_node_id} のコミュニティが同じです、そのためそのままホップします"
            )
            return True
        # 次のコミュニティで、始点コミュニティがどのグループに属しているかを調べる
        # 各コミュニティはいくつかのグループに分かれており、そのグループごとにNGリストがある。
        # 例: コミュニティ 2 には Group 1 と Group 2 があり、それぞれ別のNGリストを持つ
        # deubug
        print(f"ここからデバック next_community: {next_community}")
        print("community_groups:")
        for comm, groups in self.community_groups.items():
            print(f"  Community {comm}:")
            for group, nodes in groups.items():
                print(f"    Group {group}: Nodes {nodes}")

        # 始点コミュニティ (start_node_community) も出力
        print(f"start_node_community: {start_node_community}")

        # 始点グループを取得
        for group, nodes in self.community_groups[next_community].items():
            if start_node_community in nodes:
                belong_role = group  # 始点コミュニティが所属するグループを保存
                break

        # 　ここでNGリストを初期化する、コミュニティを移動したので参照すべきリストも変わる
        self.previous_ng_list = []

        # 始点グループを表示
        print(f"belong role: {belong_role}")
        belong_role_number = int(belong_role.split()[1])  # "Group 2" から 2 を取り出す
        # print(f"始点グループの番号: {belong_role_number}")

        # NGリストから、次のコミュニティで始点グループに対応するリストを取得
        group_ng_list = self.ng_list.get(next_community, {}).get(belong_role_number, [])
        self.previous_ng_list = group_ng_list  # ------------------------------
        # print(f"始点グループ {belong_role} のNGリスト: {group_ng_list}")  # あとで消す

        # NGリストの全体を表示
        # print(
        #     f"次のコミュニティ {next_community} のNGリスト: {self.ng_list.get(next_community, {})}"
        # )
        # 指定したコミュニティのNGリストから、特定のグループのノードリストを取得
        group_ng_list = self.ng_list.get(next_community, {}).get(belong_role_number, [])

        # 特定のグループのNGリストが存在するかを確認
        if group_ng_list is None or not group_ng_list:
            print(
                f"次のコミュニティ {next_community} のグループ {belong_role} に対するNGリストが見つかりません"
            )
            group_ng_list = []  # NGリストが見つからなかった場合は空リストを使用
        else:
            print(f"始点グループ {belong_role} のNGリスト: {group_ng_list}")

        # 次ノードの確認
        if next_node_id in group_ng_list:
            print(
                f"次ノード {next_node_id} は次コミュニティ {next_community} のグループ {belong_role} でNGです"
            )
            # TODO: ここだけFalseなので少なくなるとしたらここ-----------------------------------------------------------------
            # return False
        else:
            print(
                f"次ノード {next_node_id} はNGリストに含まれていません。ホップ可能です。"
            )
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
        print("random_walkの関数が開始")
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
            print("aaaaaaaaaaa")
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
                    print("RWが終了しました")
                    break

                # 次に選択しているnodeが有効かを確認
                # print("current_node.id", current_node.id)

                # コミュニティとNGチェック
                # print("start_node", start_node_id)
                # コミュニティとNGチェック

                # start_nodeとそのほかが同じ場合は、もともとのリストを探索する
                # 次ノードが移動可能かチェック
                # TODO:kここで認可を行うーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
                start_time_determinate = time.perf_counter()  # 時間を計測
                source_community = self.node_community_mapping.get(start_node_id)
                print(f"source_community: {source_community}")
                if not self.determine_next_hop(
                    source_community, int(current_node.id), start_node_community
                ):
                    print(
                        f"RWが一番初めにスタートしたComは{start_node_community}です。Roleを確認したところノード {current_node.id} へのホップはNGです。次のノードを選びます。"
                    )
                    continue  # NGの場合、次のノードに移動しないで再度選択
                end_time_determinate = time.perf_counter()  # 時間を計測
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
            save_notify_log(source_id, end_walk, self.total_determinate_ng_nodes)

        return end_walk, escaped_walk, self.all_paths
