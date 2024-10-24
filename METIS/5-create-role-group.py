"""
3で生成されるコミュニティごとのグループを作成から、それぞれのロール分けとNGノードの選択を行う

出力
all_dynamic
ng_node

ファイル名を変更する
community_a->server_abilene03

空行がないように気を付けること！！！
ここでの出力をP2pのKarate/datasetに適用する
"""

import os
import random
from collections import defaultdict

# ファイルリストを指定
file_numbers = ["abilene03", "abilene06", "abilene11"]  # ファイル番号のリスト
base_path = "./fb-caltech-connected/"


# 複数ファイルからノードとコミュニティを読み込む関数
def load_node_community_from_multiple_files(file_numbers, base_path):
    all_node_community = {}  # すべてのノードとコミュニティを統合
    for number in file_numbers:
        file_path = os.path.join(base_path, f"server_{number}_edges_community.txt")
        node_community = load_node_community(file_path)
        all_node_community.update(node_community)  # 統合
    return all_node_community


# ノードとコミュニティをファイルから読み込む関数
def load_node_community(file_path):
    node_community = {}
    with open(file_path, "r") as file:
        for line in file:
            node, community = map(int, line.strip().split())
            node_community[node] = community
    return node_community


# 複数ファイルのすべてのコミュニティに対してRoleを割り当てる関数
def dynamic_grouping_by_community_for_multiple_files(node_community):
    communities = set(node_community.values())  # 全コミュニティの集合
    community_group_mapping = {}

    for community in communities:
        other_communities = [
            c for c in communities if c != community
        ]  # 自分以外のすべてのコミュニティ
        if other_communities:
            groups = create_random_groups(other_communities)
            community_group_mapping[community] = {
                f"Group {i + 1}": group for i, group in enumerate(groups)
            }
    return community_group_mapping


# ランダムに1〜2のグループにコミュニティを分ける関数
def create_random_groups(communities, min_groups=1, max_groups=2):
    num_groups = random.randint(min_groups, max_groups)
    random.shuffle(communities)
    group_size = len(communities) // num_groups
    remainder = len(communities) % num_groups

    groups = []
    start = 0
    for i in range(num_groups):
        end = start + group_size + (1 if i < remainder else 0)
        groups.append(communities[start:end])
        start = end

    return groups


# 動的グループ分けをファイルに書き込む関数
def write_dynamic_groups_to_file(community_group_mapping, file_path):
    with open(file_path, "w") as file:
        for community, groups in community_group_mapping.items():
            file.write(f"Community {community}:\n")
            for group_name, group in groups.items():
                group_str = ", ".join(map(str, group))
                file.write(f"  {group_name}: {group_str}\n")
            file.write("\n")  # コミュニティごとに改行


# NGノードを選択する関数
def select_ng_nodes_per_group(community_group_mapping, node_community, percentage=0.05):
    ng_nodes_per_community = {}

    for community, groups in community_group_mapping.items():
        group_nodes = {
            group_name: [
                node
                for node, comm in node_community.items()
                if comm == community and group_name in groups
            ]
            for group_name in groups.keys()
        }

        ng_nodes_for_community = defaultdict(list)

        for group_name, nodes in group_nodes.items():
            for other_group_name, other_nodes in group_nodes.items():
                if group_name == other_group_name:
                    continue  # 同じグループに対してはNGノードを選ばない
                num_to_select = max(
                    1, int(len(nodes) * percentage)
                )  # 指定された割合で選択
                selected_ng_nodes = random.sample(nodes, num_to_select)
                ng_nodes_for_community[other_group_name].extend(selected_ng_nodes)

        ng_nodes_per_community[community] = ng_nodes_for_community

    return ng_nodes_per_community


# NGノードをファイルに書き込む関数
def write_ng_nodes_per_community_to_file(ng_nodes_per_community, file_path):
    with open(file_path, "w") as file:
        for community, ng_nodes_for_groups in ng_nodes_per_community.items():
            file.write(f"コミュニティ {community}:\n")
            sorted_groups = sorted(ng_nodes_for_groups.keys())
            for group_name in sorted_groups:
                ng_nodes = ng_nodes_for_groups[group_name]
                ng_node_str = ", ".join(map(str, ng_nodes))
                file.write(f"  NG for {group_name}: {ng_node_str}\n")
            file.write("\n")  # コミュニティごとに改行


# 実行処理部分
def process_multiple_files(file_numbers, base_path):
    # 全ファイルからノードとコミュニティを統合的に読み込む
    all_node_community = load_node_community_from_multiple_files(
        file_numbers, base_path
    )

    # 全ファイルに含まれるすべてのコミュニティにRoleを割り当て
    community_group_mapping = dynamic_grouping_by_community_for_multiple_files(
        all_node_community
    )

    # 出力ファイルに動的グループを書き込む
    output_file_path = os.path.join(base_path, "all_dynamic_groups.txt")
    write_dynamic_groups_to_file(community_group_mapping, output_file_path)

    # NGノードを選択して出力ファイルに書き込む
    ng_nodes_per_community = select_ng_nodes_per_group(
        community_group_mapping, all_node_community
    )
    ng_output_file_path = os.path.join(base_path, "ng_nodes.txt")
    write_ng_nodes_per_community_to_file(ng_nodes_per_community, ng_output_file_path)


# 実行
process_multiple_files(file_numbers, base_path)
