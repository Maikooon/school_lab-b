import networkx as nx
import csv

# 隣接行列の読み込み (edgelist.txtを例とする)
G = nx.read_edgelist("./Louvain/graph/karate.gr", nodetype=int)

# コミュニティ情報の読み込み (community.csvを例とする)
community_map = {}
with open("community.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        node, community = map(int, row)
        community_map[node] = community

# コミュニティごとのノードのリストを作成
communities = {}
for node, community in community_map.items():
    communities.setdefault(community, set()).add(node)

# モジュラリティの計算
modularity = nx.community.modularity(G, list(communities.values()))

print("モジュラリティ:", modularity)
