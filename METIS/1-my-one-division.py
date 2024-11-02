"""'
ここで自分で勝手にコミュニティを分割できるようにする
入力
グラフのエッジファイル(Louvanから撮ってくる)
出力
コミュニティ情報のファイル



に種類のファイルがあるので試す

"""

import networkx as nx
from networkx.algorithms.community import girvan_newman
from itertools import islice

# 今回分割するグラフのエッジファイルを指定
GRAPH = "fb-caltech-connected"
edge_file = f"./../Louvain/graph/{GRAPH}.gr"
OUTPUT_FILE = f"./by-my-own-division/{GRAPH}/node_community.txt"
n_communities = 2  # 分割したいコミュニティの数を指定


def calc_community_girvan_newman(edge_file, n_communities):
    # グラフの読み込み
    G = nx.read_edgelist(edge_file, nodetype=int)

    # Girvan-Newmanアルゴリズムによるコミュニティ検出
    communities_generator = girvan_newman(G)
    communities = list(islice(communities_generator, n_communities - 1, n_communities))[
        0
    ]

    # ノードと対応するコミュニティ番号をマップに作成
    community_map = {}
    for community_id, community in enumerate(communities):
        for node in community:
            community_map[node] = community_id

    # コミュニティをファイルに出力
    with open(OUTPUT_FILE, "w") as f:
        for node, community in community_map.items():
            f.write(f"{node} {community}\n")

    print(f"コミュニティ割り当て結果が '{OUTPUT_FILE}' に保存されました。")

    # コミュニティ間の接続性チェック
    all_connected = True
    for comm1, comm2 in combinations(communities, 2):
        # コミュニティ同士にエッジがあるか確認
        if not any(G.has_edge(node1, node2) for node1 in comm1 for node2 in comm2):
            all_connected = False
            print(
                f"コミュニティ {list(comm1)} とコミュニティ {list(comm2)} の間にエッジがありません。"
            )
            break

    if all_connected:
        print("すべてのコミュニティは少なくとも1本のエッジで接続されています。")
    else:
        print("一部のコミュニティ間でエッジの接続がありません。")

    # モジュラリティの計算
    modularity = nx.community.modularity(G, [list(c) for c in communities])
    print(f"モジュラリティ: {modularity}")
    return OUTPUT_FILE, modularity


calc_community_girvan_newman(edge_file, n_communities)
