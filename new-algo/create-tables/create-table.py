"""
コミュニティからNGグループを作成する

入力
エッジグラフ
コミュニティグラフ
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict


GRAPH = "fb-pages-company"  # ニコしたも修正する

# Louvainでやる時
node_community_file = f"./../../Louvain/community/{GRAPH}.cm"

# METISでやる時
# node_community_file = f"./result/{GRAPH}/node_community.txt"

# エッジファイルを読み込む
edges_file = f"./../../Louvain/graph/{GRAPH}.gr"

# node_community_file = "./../divide-community/3_communities.txt"
# edges_file = "./../../Louvain/graph/ns.gr"

output_file = "external_neighbors.txt"
group_output_file = "grouped_communities.txt"


# ノードとコミュニティをファイルから読み込む関数
def load_node_community(file_path):
    node_community = {}
    with open(file_path, "r") as file:
        for line in file:
            node, community = map(int, line.strip().split())
            node_community[node] = community
    return node_community


# エッジデータをファイルから読み込む関数
def load_edges(file_path):
    edges = []
    with open(file_path, "r") as file:
        for line in file:
            # 空行をスキップ
            if not line.strip():
                continue
            node1, node2 = map(int, line.strip().split())
            edges.append((node1, node2))
    return edges


# ランダムに2〜3のグループにコミュニティを分ける関数
def create_random_groups(communities, min_groups=2, max_groups=3):
    num_groups = random.randint(
        min_groups, max_groups
    )  # ランダムに2〜3のグループ数を選ぶ
    random.shuffle(communities)  # コミュニティの順序をランダム化
    group_size = len(communities) // num_groups  # 各グループの基本サイズ
    remainder = len(communities) % num_groups  # グループ数に割り切れない場合の余り

    groups = []
    start = 0
    for i in range(num_groups):
        # 各グループには少なくとも1つのコミュニティが含まれるようにする
        end = start + group_size + (1 if i < remainder else 0)
        groups.append(communities[start:end])
        start = end

    return groups


# 動的に各コミュニティに対してグループを作成する関数
def dynamic_grouping_by_community(node_community):
    communities = set(node_community.values())  # コミュニティの集合
    community_group_mapping = {}

    for community in communities:
        other_communities = [
            c for c in communities if c != community
        ]  # 自分以外のコミュニティ
        if other_communities:
            groups = create_random_groups(other_communities)
            community_group_mapping[community] = {
                f"Group {i + 1}": group for i, group in enumerate(groups)
            }
    return community_group_mapping


# わかりやすい方の出力方法
# 動的グループ分けをファイルに書き込む関数
def write_dynamic_groups_to_file(community_group_mapping, file_path):
    with open(file_path, "w") as file:
        for community, groups in community_group_mapping.items():
            file.write(f"Community {community}:\n")
            for group_name, group in groups.items():
                group_str = ", ".join(map(str, group))
                file.write(f"  {group_name}: {group_str}\n")
            file.write("\n")  # コミュニティごとに改行


# def write_dynamic_groups_to_file(community_group_mapping, file_path):
#     with open(file_path, "w") as file:
#         for community, groups in community_group_mapping.items():
#             for group_name, group in groups.items():
#                 file.write(f"{community}")
#                 group_str = " ".join(map(str, group))
#                 group_name = group_name[6]
#                 file.write(f" {group_name} {group_str}\n")
#             file.write("\n")  # コミュニティごとに改行


# グループ分けされたコミュニティでNGノードを選択する関数
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
# わかりやすく出力する方法
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


# 簡略化した出力方法
# def write_ng_nodes_per_community_to_file(ng_nodes_per_community, file_path):
#     with open(file_path, "w") as file:
#         for community, ng_nodes_for_groups in ng_nodes_per_community.items():
#             sorted_groups = sorted(ng_nodes_for_groups.keys())
#             for group_name in sorted_groups:
#                 ng_nodes = ng_nodes_for_groups[group_name]
#                 ng_node_str = " ".join(map(str, ng_nodes))
#                 shortened_group_name = group_name[6:]
#                 file.write(f"{community} {shortened_group_name} {ng_node_str}\n")
#             file.write("\n")


# コミュニティに基づいてノードをグループに分ける関数
def group_nodes_by_community(node_community, community_group_mapping):
    grouped_nodes = defaultdict(list)

    for node, community in node_community.items():
        if community in community_group_mapping:
            group_definitions = community_group_mapping[community]
            for group_name, group_communities in group_definitions.items():
                if community in group_communities:
                    grouped_nodes[group_name].append(node)
    print(grouped_nodes)
    return grouped_nodes


# グループの結果を書き込む
def write_groups_to_file(groups, group_output_file):
    with open(group_output_file, "w") as file:
        for group_name, nodes in groups.items():
            file.write(f"{group_name}: {nodes}\n")


# グループからノードをランダムに選び出す関数、全体の１０％ほどになればok
def select_random_nodes(groups, percentage=0.1):
    selected_nodes = {}

    for group_name, group_nodes in groups.items():
        num_to_select = max(
            1, int(len(group_nodes) * percentage)
        )  # 10%を計算し、少なくとも1つ選ぶ
        selected_nodes[group_name] = random.sample(group_nodes, num_to_select)

    return selected_nodes


# 選択したノードをファイルに書き込む関数
def write_selected_nodes_to_file(selected_nodes, output_file):
    with open(output_file, "w") as file:
        for group_name, nodes in selected_nodes.items():
            file.write(f"{group_name}: {nodes}\n")


# データを読み込む
node_community = load_node_community(node_community_file)
edges = load_edges(edges_file)

# グラフの作成
G = nx.Graph()

# ノードとエッジを追加
G.add_nodes_from(node_community)
G.add_edges_from(edges)

# # 異なるコミュニティの隣接ノードを検索
# external_neighbors = find_external_neighbors(G, node_community)

# # 結果をファイルに書き込み
# write_external_neighbors_to_file(external_neighbors, output_file)

# 各コミュニティに基づいてノードをグループに分ける
community_group_mapping = dynamic_grouping_by_community(node_community)
write_dynamic_groups_to_file(
    community_group_mapping, f"./result/{GRAPH}/dynamic_groups.txt"
)

select_ng_nodes_per_group = select_ng_nodes_per_group(
    community_group_mapping, node_community
)
write_ng_nodes_per_community_to_file(
    select_ng_nodes_per_group, f"./result/{GRAPH}/ng_nodes.txt"
)
