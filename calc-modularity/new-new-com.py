import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# 1. グラフ生成
num_nodes = 762  # ノード数
num_edges = 16651  # エッジ数
COMMUNITY = 12


G = nx.gnm_random_graph(num_nodes, num_edges)

# 2. Louvain法でコミュニティ分割
partition = community_louvain.best_partition(G)

# 3. クラスタリングで指定したコミュニティ数に分割 (例: 12コミュニティ)
pos = nx.spring_layout(G)
pos_array = np.array([pos[n] for n in G.nodes()])
kmeans = KMeans(n_clusters=COMMUNITY, random_state=0)
kmeans.fit(pos_array)
labels = kmeans.labels_

# 4. グラフ描画
cmap = plt.get_cmap("viridis")
nx.draw_networkx_nodes(G, pos, node_color=labels, node_size=40, cmap=cmap)
nx.draw_networkx_edges(G, pos, alpha=0.5)
# plt.show()

# 5. ノードとそのコミュニティをファイルに格納
output_file = "./new-new-community/" + str(COMMUNITY) + "_communities.txt"
with open(output_file, "w") as f:
    for node in G.nodes():
        community = partition[node]  # Louvainコミュニティ
        f.write(f"{node} {community}\n")

print(f"ノードとそのコミュニティは {output_file} に保存されました。")


# Q;　i wanna change  int to str
# A: change int to str   (COMMUNITY) -> str(COMMUNITY)  in line 52
