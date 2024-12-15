"""
Louvainで与えられたグラフとMETISで分割したグラフに対してIPを振り当てる
abileneサーバごとにエッジにIPを振り当てる


INPUT_FILE = f"./by-my-own-division/{GRAPH}/node_community.txt"
OUTPUT_FILE = f"./by-my-own-division/{GRAPH}/community_{community_id}.txt"

出力
以下に出力されるので、名前を変更する
community_0.txt ->abilene03.txt
community_1.txt ->abilene06.txt
community_2.txt ->abilene11.txt
"""

import os

# GRAPH = "fb-caltech-connected"
GRAPH = os.getenv("GRAPH", "fb-caltech-connected")

# Louvainのとき　　　これはまだ使用していない(それだけのサーバを用意できていないため)
# community_file = "./../../Louvain/community/karate.tcm"

# METISの時
# community_file = "./by-METIS/" + GRAPH + "/node_community.txt"

# そのたのとき
# community_file = "./by-my-own-division/" + GRAPH + "/node_community.txt"
community_file = "./" + GRAPH + "/3node_community.txt"

edge_file = "./../Louvain/graph/" + GRAPH + ".gr"

# コミュニティごとのIPアドレスのマッピング
ip_mapping = {
    0: "10.58.60.3",
    1: "10.58.60.6",
    2: "10.58.60.11",
    # 3: "10.58.60.12",
    # 4: "10.58.60.13",
    # 5: "10.58.60.14",
    # 6: "10.58.60.15",
    # 7: "10.58.60.16",
    # 8: "10.58.60.17",
    # 9: "10.58.60.18",
}
# server_name = {"abilene03", "abilene06", "abilene11"}
server_name = {
    "abilene03",
    "abilene06",
    "abilene11",
    # "abilene12",
    # "abilene13",
    # "abilene14",
    # "abilene15",
    # "abilene16",
    # "abilene17",
    # "abilene18",
}


# コミュニティ情報の読み込み
def read_communities(file_path):
    communities = {}
    with open(file_path, "r") as f:
        for line in f:
            node, community = map(int, line.split())
            if community not in communities:
                communities[community] = []
            communities[community].append(node)
    return communities


# エッジ情報の読み込み
def read_edges(file_path):
    edges = []
    with open(file_path, "r") as f:
        for line in f:
            node1, node2 = map(int, line.split())
            edges.append((node1, node2))
    return edges


# IP付きのグラフを生成し、コミュニティごとにファイルに出力
def generate_and_save_ip_graph(communities, edges):
    ip_graph = {}

    # コミュニティの初期化
    for community_id in communities.keys():
        ip_graph[community_id] = []

    # コミュニティ内の接続を追加
    for community_id, nodes in communities.items():
        for node1 in nodes:
            for node2 in nodes:
                if node1 != node2 and (
                    (node1, node2) in edges or (node2, node1) in edges
                ):
                    ip_graph[community_id].append(
                        f"{node1},{node2},{ip_mapping[community_id]}"
                    )

    # コミュニティ間の接続を追加
    try:
        for node1, node2 in edges:
            community1 = next(c for c, n in communities.items() if node1 in n)
            community2 = next(c for c, n in communities.items() if node2 in n)

            # コミュニティが異なる場合

            if community1 != community2:
                ip_graph[community1].append(f"{node1},{node2},{ip_mapping[community2]}")
                ip_graph[community2].append(f"{node2},{node1},{ip_mapping[community1]}")
    except StopIteration:
        print(
            f"Warning: One of the nodes {node1} or {node2} does not belong to any community."
        )

    # コミュニティごとにファイルを書き込む
    for community_id, edges in ip_graph.items():
        file_name = (
            "./" + GRAPH + f"/community_{community_id}.txt"
        )  # コミュニティごとのファイル名
        with open(file_name, "w") as f:
            for edge in edges:
                f.write(f"{edge}\n")  # エッジ情報をファイルに書き込み

    print("各コミュニティのファイルが生成されました。")


communities = read_communities(community_file)
edges = read_edges(edge_file)

# IP付きのグラフを生成し、ファイルに保存
generate_and_save_ip_graph(communities, edges)
