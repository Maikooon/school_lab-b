import networkx as nx
import matplotlib.pyplot as plt


# ファイルからエッジリストを読み込む関数
def load_edges_from_file(file_path):
    edges = []
    with open(file_path, "r") as file:
        for line in file:
            # 各行を空白で分割して、タプルとしてエッジを作成
            node1, node2 = map(int, line.strip().split())
            edges.append((node1, node2))
    return edges


# エッジリストのファイルパスを指定
file_path = "./Louvain/graph/karate.gr"

# ファイルからエッジリストを読み込む
edges = load_edges_from_file(file_path)

# グラフ構築
G = nx.Graph()
G.add_edges_from(edges)

# コミュニティ別にノードを定義（手動で分割された結果）
community_nodes = [
    {0, 1, 2, 6, 7, 8, 10, 15, 16, 24, 27, 33, 21, 18},  # コミュニティ1
    {3, 4, 9, 14, 19, 25, 30, 31, 32},  # コミュニティ2
    {5, 11, 12, 13, 17, 20, 22, 23, 26, 28, 29},  # コミュニティ3
]

# 各コミュニティのエッジを取得して出力
for i, community in enumerate(community_nodes):
    subgraph = G.subgraph(community)
    print(f"コミュニティ {i+1}:")
    print(f"  ノード: {sorted(community)}")
    print(f"  エッジ: {sorted(subgraph.edges)}\n")

# 色リスト（コミュニティごとに異なる色）
colors = ["red", "blue", "green"]

# コミュニティごとにノードの色を割り当て
community_colors = {}
for i, community in enumerate(community_nodes):
    for node in community:
        community_colors[node] = colors[i]

# コミュニティごとにノードを配置
pos = {}
for i, community in enumerate(community_nodes):
    # コミュニティ内のノードをspring_layoutで配置
    subgraph = G.subgraph(community)
    sub_pos = nx.spring_layout(subgraph, seed=42)  # 固定レイアウト
    # コミュニティの位置を全体の位置に統合
    for node, p in sub_pos.items():
        pos[node] = p + 2 * i  # コミュニティごとにx座標をずらして配置

# ノードの色リストを作成
node_colors = [community_colors[node] for node in G.nodes()]

# グラフをプロット
plt.figure(figsize=(12, 8))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=node_colors,
    node_size=500,
    edge_color="gray",
    font_size=10,
)

# タイトルを追加
plt.title("コミュニティ別に色分けしたグラフ (コミュニティごとに配置)", fontsize=16)
plt.savefig("community_graph_karate.png")
plt.show()
