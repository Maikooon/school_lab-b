import networkx as nx
import random


def load_edges_from_file(file_path):
    edges = []
    with open(file_path, "r") as file:
        for line in file:
            # 各行を空白で分割して、タプルとしてエッジを作成
            node1, node2 = map(int, line.strip().split())
            edges.append((node1, node2))
    return edges


# グラフ構築
G = nx.Graph()
# エッジリストのファイルパスを指定
file_path = "./Louvain/graph/fb-caltech-connected.gr"

# ファイルからエッジリストを読み込む
edges = load_edges_from_file(file_path)
G.add_edges_from(edges)

# ノードのランダム分割
nodes = list(G.nodes())
random.shuffle(nodes)
k = 3  # コミュニティ数
community_nodes = [set() for _ in range(k)]

for i, node in enumerate(nodes):
    community_nodes[i % k].add(node)

# 出力用のファイルを指定
output_file_path = "./community_output.txt"

with open(output_file_path, "w") as output_file:
    # 各コミュニティのエッジを取得して出力
    for i, community in enumerate(community_nodes):
        subgraph = G.subgraph(community)
        output_file.write(f"コミュニティ {i+1}:\n")
        output_file.write(f"  ノード: {sorted(community)}\n")
        output_file.write(f"  エッジ: {sorted(subgraph.edges)}\n\n")

    # 計算されたコミュニティのノード情報を以下の形式で出力
    output_file.write("# 計算されたコミュニティのノード定義\n")
    output_file.write("community_nodes = [\n")
    for community in community_nodes:
        output_file.write(f"    {sorted(community)},\n")
    output_file.write("]\n")

print(f"結果は {output_file_path} に保存されました。")
