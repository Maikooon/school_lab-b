import networkx as nx
import os


# EDGE_FILE = "./../Louvain/graph/karate.gr"
# COMMUNITY_FILE = "./../Louvain/community/karate.tcm"

edge_file_list = [
    "ca-grqc-connected.gr",
    "cmu.gr",
    "com-amazon-connected.gr",
    "email-enron-connected.gr",
    "fb-caltech-connected.gr",
    "fb-pages-company.gr",
    "karate-graph.gr",
    "karate.gr",
    "rt-retweet.gr",
    "simple_graph.gr",
    "soc-slashdot.gr",
    "tmp.gr",
]


community_file_list = [
    "ca-grqc-connected.cm",
    "cmu.cm",
    "com-amazon-connected.cm",
    "email-enron-connected.cm",
    "fb-caltech-connected.cm",
    "fb-pages-company.cm",
    "karate-graph.cm",
    "karate.tcm",
    "rt-retweet.cm",
    "simple_graph.cm",
    "soc-slashdot.cm",
    "tmp.cm",
]


def calc(edge_file, community_file, filename):
    # 隣接行列の読み込み
    G = nx.read_edgelist(edge_file, nodetype=int)

    # コミュニティ情報の読み込み
    community_map = {}
    with open(community_file, "r") as f:
        for line in f:
            row = line.strip().split()
            node, community = map(int, row)
            community_map[node] = community

    # コミュニティごとのノードのリストを作成
    communities = {}
    for node, community in community_map.items():
        communities.setdefault(community, set()).add(node)

    # モジュラリティの計算
    modularity = nx.community.modularity(G, list(communities.values()))

    print(filename, ":", modularity)


def main():
    for i in range(len(edge_file_list)):
        edge_file = "./../Louvain/graph/" + edge_file_list[i]
        community_file = "./../Louvain/community/" + community_file_list[i]
        filename_with_ext = os.path.basename(
            edge_file
        )  # ファイル名（拡張子付き）を取得
        filename = os.path.splitext(filename_with_ext)[0]  # 拡張子を除去
        calc(edge_file, community_file, filename)


main()
