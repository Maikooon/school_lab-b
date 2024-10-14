# """_summary_

# new

# """

# import networkx as nx
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import random
# from collections import defaultdict

# # ファイルからデータを読み込み
# # node_community_file = "./divide-community/3_communities.txt"
# # edges_file = "./../Louvain/graph/ns.gr"

# node_community_file = "./../Louvain/community/karate.tcm"
# edges_file = "./../Louvain/graph/karate.gr"

# output_file = "external_neighbors.txt"
# group_output_file = "grouped_communities.txt"
# output_file_selected_nodes = "selected_nodes.txt"
# output_ng_nodes_file = "ng_nodes.txt"  # NGノードを記録するファイル


# # ノードとコミュニティをファイルから読み込む関数
# def load_node_community(file_path):
#     node_community = {}
#     with open(file_path, "r") as file:
#         for line in file:
#             node, community = map(int, line.strip().split())
#             node_community[node] = community
#     return node_community


# # エッジデータをファイルから読み込む関数
# def load_edges(file_path):
#     edges = []
#     with open(file_path, "r") as file:
#         for line in file:
#             if not line.strip():
#                 continue
#             node1, node2 = map(int, line.strip().split())
#             edges.append((node1, node2))
#     return edges


# # 異なるコミュニティの隣接ノードを調べる関数
# def find_external_neighbors(G, node_community):
#     external_neighbors = defaultdict(list)  # 外部隣接ノードを保持する辞書
#     for node in G.nodes():
#         current_community = node_community[node]
#         for neighbor in G.neighbors(node):
#             neighbor_community = node_community[neighbor]
#             if (
#                 neighbor_community != current_community
#             ):  # 隣接ノードが異なるコミュニティに属するか確認
#                 external_neighbors[node].append((neighbor, neighbor_community))
#     return external_neighbors


# # 結果をファイルに書き込む関数
# def write_external_neighbors_to_file(external_neighbors, output_file, node_community):
#     with open(output_file, "w") as file:
#         for node, neighbors in external_neighbors.items():
#             file.write(
#                 f"Node {node} (Community {node_community[node]}) is connected to:\n"
#             )
#             for neighbor, community in neighbors:
#                 file.write(f"  - Node {neighbor} (Community {community})\n")


# # コミュニティをグループに分ける関数
# def group_communities(node_community):
#     communities = list(
#         set(node_community.values())
#     )  # ユニークなコミュニティのリストを取得
#     random.shuffle(communities)  # コミュニティをシャッフル
#     groups = []
#     while communities:
#         group_size = random.randint(1, 3)  # 1〜3の間でグループサイズを決定
#         group = communities[:group_size]  # コミュニティをグループに追加
#         groups.append(group)
#         communities = communities[group_size:]  # 残りのコミュニティを更新
#     return groups


# # グループ分けの結果を書き込む
# def write_groups_to_file(groups, group_output_file):
#     with open(group_output_file, "w") as file:
#         for i, group in enumerate(groups):
#             file.write(f"Group {i + 1}: {group}\n")


# # グループごとに他のグループに対するNGノードを選ぶ
# def select_ng_nodes(groups, node_community, percentage=0.05):
#     ng_nodes = defaultdict(lambda: defaultdict(list))  # NGノードを保持する辞書
#     for i, group in enumerate(groups):
#         group_nodes = [node for node, comm in node_community.items() if comm in group]
#         for j, other_group in enumerate(groups):
#             if i == j:
#                 continue  # 同じグループに対してはNGノードを選ばない
#             num_to_select = max(1, int(len(group_nodes) * percentage))  # 5%を選ぶ
#             selected_ng_nodes = random.sample(group_nodes, num_to_select)
#             ng_nodes[f"Group {i + 1}"][f"Group {j + 1}"] = selected_ng_nodes
#     return ng_nodes


# # NGノードをファイルに書き込む
# def write_ng_nodes_to_file(ng_nodes, output_ng_nodes_file):
#     with open(output_ng_nodes_file, "w") as file:
#         for group, ng_for_groups in ng_nodes.items():
#             file.write(f"{group}:\n")
#             for target_group, nodes in ng_for_groups.items():
#                 file.write(f"  NG for {target_group}: {', '.join(map(str, nodes))}\n")


# # グラフの作成
# def create_graph(node_community, edges):
#     G = nx.Graph()
#     G.add_nodes_from(node_community)
#     G.add_edges_from(edges)
#     return G


# # メイン処理
# def main():
#     node_community = load_node_community(node_community_file)
#     edges = load_edges(edges_file)

#     # グラフの作成
#     G = create_graph(node_community, edges)

#     # 異なるコミュニティの隣接ノードを検索
#     external_neighbors = find_external_neighbors(G, node_community)
#     write_external_neighbors_to_file(external_neighbors, output_file, node_community)

#     # コミュニティのグループ分け
#     groups = group_communities(node_community)
#     write_groups_to_file(groups, group_output_file)

#     # グループからノードをランダムに選び出す
#     # selected_nodes = select_random_nodes(groups, node_community, percentage=0.1)
#     # write_selected_nodes_to_file(selected_nodes, output_file_selected_nodes)

#     # NGノードの選定と書き出し
#     ng_nodes = select_ng_nodes(groups, node_community, percentage=0.05)
#     write_ng_nodes_to_file(ng_nodes, output_ng_nodes_file)

#     # コミュニティごとのグラフを描画（オプション）
#     draw_graph(G, node_community)


# # グラフ描画（オプション）
# def draw_graph(G, node_community):
#     communities = set(node_community.values())
#     num_communities = len(communities)
#     colormap = cm.get_cmap("tab20", num_communities)
#     colors = {community: colormap(i) for i, community in enumerate(communities)}
#     node_colors = [colors[node_community[node]] for node in G.nodes()]
#     pos = nx.spring_layout(G)
#     nx.draw(
#         G,
#         pos,
#         with_labels=True,
#         node_color=node_colors,
#         node_size=800,
#         font_size=16,
#         font_color="white",
#         edge_color="gray",
#     )
#     plt.show()


# # 実行
# if __name__ == "__main__":
#     main()
