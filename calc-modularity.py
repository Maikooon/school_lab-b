import networkx as nx
import os
from collections import Counter

edge_file_list = [
    # "ca-grqc-connected.gr",
    # "fb-caltech-connected.gr",
    "fb-pages-company.gr",
    # "karate.gr",
]

community_file_list = [
    # "METIS-ca",
    # "METIS-fb-caltech",
    # "METIS-fb-pages",
    # "METIS-karate",
    # "my-ca",
    "my-fb-pages",
    # "my-fb-caltech",
    # "my-karate",
]


def calc(edge_file, community_file, filename):
    # グラフの読み込み
    G = nx.read_edgelist(edge_file, nodetype=int)

    # コミュニティ情報の読み込み
    community_map = {}
    with open(community_file, "r") as f:
        for line in f:
            row = line.strip().split()
            node, community = map(int, row)
            community_map[node] = community

    # コミュニティごとのノードリスト作成
    communities = {}
    for node, community in community_map.items():
        communities.setdefault(community, set()).add(node)

    # グラフ内のすべてのノードがコミュニティに含まれているか確認
    all_nodes_in_communities = set(
        node for community in communities.values() for node in community
    )
    missing_nodes = set(G.nodes()) - all_nodes_in_communities

    # 含まれていないノードを新しいコミュニティに追加
    if missing_nodes:
        new_community_id = max(communities.keys()) + 1
        communities[new_community_id] = missing_nodes
        print(f"{filename}: Added missing nodes to new community {new_community_id}")

    # 重複ノードの解消
    node_counts = Counter(
        node for community in communities.values() for node in community
    )
    duplicate_nodes = [node for node, count in node_counts.items() if count > 1]

    for node in duplicate_nodes:
        first_community = next(
            community for community, nodes in communities.items() if node in nodes
        )
        for community, nodes in communities.items():
            if community != first_community and node in nodes:
                nodes.remove(node)
        print(
            f"{filename}: Resolved duplicates, kept node {node} in community {first_community}"
        )

    # モジュラリティ計算を試行
    try:
        modularity = nx.community.modularity(G, list(communities.values()))
        print(filename, ":", modularity)
    except nx.NetworkXError as e:
        print(f"{filename}: Error calculating modularity - {e}")
        # 必要に応じてエラー処理を追加可能
        print("Skipping modularity calculation for this graph due to partition issue.")


def main():
    for i in range(len(edge_file_list)):
        community_file = (
            "./new-algo/create-tables/result/"
            + community_file_list[i]
            + "/node_community.txt"
        )
        edge_file = "./Louvain/graph/" + edge_file_list[i]
        filename_with_ext = os.path.basename(edge_file)
        filename = os.path.splitext(filename_with_ext)[0]
        calc(edge_file, community_file, filename)


main()
