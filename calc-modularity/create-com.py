# import networkx as nx
# import numpy as np
# from fcmeans import FCM  # fuzzy-c-means ライブラリから FCM をインポート


# def calc_community(edge_file, n_clusters):
#     # グラフの読み込み
#     G = nx.read_edgelist(edge_file, nodetype=int)

#     # 隣接行列の取得
#     adj_matrix = nx.adjacency_matrix(G).todense()

#     # FCMモデルの初期化
#     fcm = FCM(n_clusters=n_clusters, random_state=0)

#     # FCMによるクラスタリング
#     fcm.fit(adj_matrix)

#     # 各ノードのクラスタ所属度合い
#     u = fcm.u

#     # コミュニティのマップを作成
#     community_map = {}
#     for i, node in enumerate(G.nodes):
#         memberships = [(j, u[i][j]) for j in range(n_clusters)]
#         memberships.sort(key=lambda x: x[1], reverse=True)
#         community_map[node] = memberships[0][0]

#     # コミュニティをファイルに出力
#     output_file = "./new_community/fb-caltech-connected.cm"
#     with open(output_file, "w") as f:
#         for node, community in community_map.items():
#             f.write(f"{node} {community}\n")

#     print(f"コミュニティ割り当て結果が '{output_file}' に保存されました。")

#     # モジュラリティの計算
#     communities = {}
#     for node, community in community_map.items():
#         communities.setdefault(community, set()).add(node)

#     modularity = nx.community.modularity(G, list(communities.values()))
#     print(f"モジュラリティ: {modularity}")


# # 実行する関数を呼び出す
# edge_file = "./../Louvain/graph/fb-caltech-connected.gr"
# n_clusters = 8  # コミュニティ数を指定
# calc_community(edge_file, n_clusters)


import networkx as nx
import numpy as np
from sklearn.cluster import KMeans


def calc_community_kmeans(edge_file, n_clusters):
    # グラフの読み込み
    G = nx.read_edgelist(edge_file, nodetype=int)

    # 隣接行列の取得
    adj_matrix = nx.adjacency_matrix(G).todense()

    # KMeansモデルの初期化
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)

    # KMeansによるクラスタリング
    kmeans.fit(adj_matrix)
    labels = kmeans.labels_

    # コミュニティのマップを作成
    community_map = {node: labels[i] for i, node in enumerate(G.nodes())}

    # コミュニティをファイルに出力
    output_file = "./new-community/rt-retweet.cm"
    with open(output_file, "w") as f:
        for node, community in community_map.items():
            f.write(f"{node} {community}\n")

    print(f"コミュニティ割り当て結果が '{output_file}' に保存されました。")

    # モジュラリティの計算
    communities = {}
    for node, community in community_map.items():
        communities.setdefault(community, set()).add(node)

    modularity = nx.community.modularity(G, list(communities.values()))
    print(f"モジュラリティ: {modularity}")
    return output_file, modularity


# 実行する関数を呼び出す
edge_file = "./../Louvain/graph/rt-retweet.gr"
n_clusters = 8  # コミュニティ数を指定
calc_community_kmeans(edge_file, n_clusters)
