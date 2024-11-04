"""'
ここで自分で勝手にコミュニティを分割できるようにする
入力
グラフのエッジファイル(Louvanから撮ってくる)
出力
コミュニティ情報のファイル
node_communityが./分割方法/グラフ名/
のフォルダ下に格納される

"""

# TODO:こちらが1種類目
import networkx as nx
import numpy as np
from sklearn.cluster import KMeans
import os

# ca-grqc-connected.gr
# 今回分割するグラフのエッジファイルを入れる
GRAPH = os.getenv("GRAPH", "cmu")
n_clusters = 3  # コミュニティ数を指定

edge_file = f"./../Louvain/graph/{GRAPH}.gr"
OUTPUT_FILE = f"./by-my-own-division/{GRAPH}/node_community.txt"


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
    output_file = OUTPUT_FILE
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


calc_community_kmeans(edge_file, n_clusters)
