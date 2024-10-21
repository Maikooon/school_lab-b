from Node import *
import random
from queue import Queue


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

    def determine_next_hop(self, source_community, next_node_id):
        # 次ノードのコミュニティIDを取得
        next_community = self.node_community_mapping.get(next_node_id)
        print(f"次ノード {next_node_id} のコミュニティID: {next_community}")
        print(f"始点コミュニティID: {source_community}")
        # 属していないということは他サーバにあるということなのでこれはなくてもいいかも？
        if next_community is None:
            print(f"次ノード {next_node_id} のコミュニティが見つかりません")
            return False
        # print(
        #     f"次コミュニティ{source_community}において、視点コミュニティはGroup９０です"
        # )
        # 次のコミュニティにおいて、始点コミュニティが属するグループを判定
        for group, nodes in self.community_groups[next_community].items():
            if source_community in nodes:
                source_group = group
                break
        else:  # TODO:この順番にすると、初めがえらるので一旦無視
            print(
                f"始点コミュニティ {source_community} が次のコミュニティ {next_community} のどのグループにも属していません"
            )
            # return False
        # NGリストの次のコミュニティの欄において、始点コミュニティのグループ欄を確認
        # 始点グループのNGリストを取得し、次ノードが含まれるか確認
        group_ng_list = self.ng_list.get(next_community, {}).get(source_group, [])
        print(
            f"始点グループ {source_group} のNGリスト: {group_ng_list}"
        )  # TODO:なんでここが空列になるのか
        if next_node_id in group_ng_list:
            print(
                f"次ノード {next_node_id} は次コミュニティ {next_community} のグループ {source_group} でNGです"
            )
            return False

        # NGに含まれていなければホップを許可
        print(f"NGに含まれていないので次ノード {next_node_id} へホップ可能")
        return True

    def random_walk(self, source_id, count, alpha=0.15, all_paths=None):
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
                    print("RWが終了しました")
                    break

                # 現在のノードが有効かを確認
                print("current_node.id", current_node.id)
                print(f"current_node.idの型: {type(current_node.id)}")

                # debug
                # ノードのIDが整数型であることを確認する
                current_node_id = int(current_node.id)
                if current_node_id not in self.node_community_mapping:
                    print(
                        f"エラー: ノード {current_node.id} に対応するコミュニティIDが見つかりません"
                    )
                    print(
                        "現在のnode_community_mappingのキー:",
                        list(self.node_community_mapping.keys()),
                    )
                    return [], {}, all_paths

                # コミュニティとNGチェック
                source_community = self.node_community_mapping[int(current_node.id)]

                # 次ノードが移動可能かチェック
                # if not self.determine_next_hop(source_community, int(current_node.id)):
                #     print(
                #         f"ノード {current_node.id} へのホップはNGです。次のノードを選びます。"
                #     )
                #     continue  # NGの場合、次のノードに移動しないで再度選択

                # 通ったノードを追加する
                self.all_paths.append(current_node.id)

                # 最後に次のノードを選択
                next_node = current_node.get_random_adjacent()

                # 次のノードを現在のノードに設定
                current_node = next_node

            print("end_walk", end_walk)
            print("escaped_walk", escaped_walk)
            print("all-paths", self.all_paths)
        return end_walk, escaped_walk, self.all_paths
