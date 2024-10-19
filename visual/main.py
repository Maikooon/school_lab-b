import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ファイルパス
community_file = "./../Louvain/community/karate.tcm"
edge_file = "./../Louvain/graph/karate.gr"

# エッジリストの読み込み
edges_df = pd.read_csv(
    edge_file, delim_whitespace=True, header=None, names=["source", "target"]
)
edges = [(row["source"], row["target"]) for index, row in edges_df.iterrows()]

# コミュニティ情報の読み込み
communities_df = pd.read_csv(
    community_file, delim_whitespace=True, header=None, names=["node", "community"]
)
communities = {
    row["node"]: row["community"] for index, row in communities_df.iterrows()
}

# グラフの作成
G = nx.Graph()
G.add_edges_from(edges)

# ノードの色をコミュニティに基づいて設定
color_map = []
for node in G.nodes():
    community_id = communities.get(node)
    if community_id == 0:
        color_map.append("lightblue")
    elif community_id == 1:
        color_map.append("lightgreen")
    elif community_id == 2:
        color_map.append("lightcoral")
    else:
        color_map.append("gray")  # コミュニティが定義されていないノード

# グラフの描画
plt.figure(figsize=(10, 8))
nx.draw(
    G,
    with_labels=True,
    node_color=color_map,
    node_size=700,
    font_size=12,
    font_color="black",
    font_weight="bold",
    edge_color="gray",
)
plt.title("Graph Visualization with Communities")
plt.show()
