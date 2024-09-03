import networkx as nx
import numpy as np
from fcmeans import FCM  # fuzzy-c-means ライブラリから FCM をインポート
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message="resource_tracker")


edge_file_list = [
    # "ca-grqc-connected.gr",
    # "cmu.gr",
    # "com-amazon-connected.gr",
    # "email-enron-connected.gr",
    # "fb-caltech-connected.gr",
    # "fb-pages-company.gr",
    # "karate-graph.gr",
    # "karate.gr",
    # "rt-retweet.gr",
    # "simple_graph.gr",
    # "soc-slashdot.gr",
    "tmp.gr",
]

community_file_list = [
    # "ca-grqc-connected.cm",
    # "cmu.cm",
    # "com-amazon-connected.cm",
    # "email-enron-connected.cm",
    # "fb-caltech-connected.cm",
    # "fb-pages-company.cm",
    # "karate-graph.cm",
    # "karate.tcm",
    # "rt-retweet.cm",
    # "simple_graph.cm",
    # "soc-slashdot.cm",
    "tmp.cm",
]


def calc(edge_file, number):
    # 出力の加工
    filename_with_ext = os.path.basename(edge_file)
    filename = os.path.splitext(filename_with_ext)[0]  # 拡張子を除去

    # 　新しいコミュニティの生成
    G = nx.read_edgelist(edge_file, nodetype=int)
    n_clusters = number  # クラスタ数
    adj_matrix = nx.adjacency_matrix(G).todense()  # グラフの隣接行列を取得
    fcm = FCM(n_clusters=n_clusters, random_state=0)  # FCMモデルの初期化
    # FCMによるクラスタリング
    fcm.fit(adj_matrix)
    u = fcm.u  # 各ノードのクラスタ所属度合い

    # 結果の表示
    community_map = {}  # ノードごとの所属クラスタを格納する辞書
    for i, node in enumerate(G.nodes):
        memberships = [(j, u[i][j]) for j in range(n_clusters)]
        memberships.sort(key=lambda x: x[1], reverse=True)  # 所属度合いでソート
        community_map[node] = memberships[0][0]
    # 結果をファイルに保存
    with open("./new_community/" + filename + ".cm", "w") as f:
        for node, community in community_map.items():
            f.write(f"{node} {community}\n")
    print("コミュニティマップが 'community_map.txt' に保存されました。")
    # この結果を踏まえて、モジュラリティを計算する
    # 隣接行列の読み込み
    G = nx.read_edgelist(edge_file, nodetype=int)

    communities = {}
    for node, community in community_map.items():
        communities.setdefault(community, set()).add(node)

    # モジュラリティの計算
    modularity = nx.community.modularity(G, list(communities.values()))

    print(filename, "Modularity:", modularity)


def count_community(community_file):
    with open(community_file, "r") as f:
        # 正しい形式でデータを読み込む
        rows = [line.strip() for line in f if line.strip()]  # 空行を除去

    # データの処理
    community_values = []
    for row in rows:
        parts = row.split()
        if len(parts) >= 2:  # 行が期待されるフォーマットであることを確認
            value = int(parts[1])
            community_values.append(value)
    count_community = max(community_values) + 1
    print(count_community)
    return count_community


def main():
    for i in range(len(edge_file_list)):
        edge_file = "./../Louvain/graph/" + edge_file_list[i]
        # 　コミュニティの数を計算する
        community_file = "./../Louvain/community/" + community_file_list[i]
        calc(edge_file, count_community(community_file))


main()
