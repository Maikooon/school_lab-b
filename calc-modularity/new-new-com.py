import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import os

# 1. グラフ生成
num_nodes = 762  # ノード数
num_edges = 16651  # エッジ数
G = nx.gnm_random_graph(num_nodes, num_edges)

# 2. Louvain法をコメントアウト（今回は使わない）
# partition = community_louvain.best_partition(G)  # Louvainコミュニティ分割は使用しない

# 3. クラスタリングで指定したコミュニティ数に分割 (例: 12コミュニティ)
COMMUNITY = 18  # クラスタ数
pos = nx.spring_layout(G)
pos_array = np.array([pos[n] for n in G.nodes()])
kmeans = KMeans(n_clusters=COMMUNITY, random_state=0)
kmeans.fit(pos_array)
labels = kmeans.labels_

# 4. グラフ描画
cmap = plt.get_cmap("viridis")
nx.draw_networkx_nodes(G, pos, node_color=labels, node_size=40, cmap=cmap)
nx.draw_networkx_edges(G, pos, alpha=0.5)
# plt.show()  # グラフ表示（必要に応じて）

# 5. ノードとそのクラスタをファイルに格納
output_folder = "./new-new-community/"
output_file = output_folder + str(COMMUNITY) + "_communities.txt"

# フォルダがなければ作成
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ノードとクラスタの情報をファイルに書き込み
with open(output_file, "w") as f:
    for node, community in zip(G.nodes(), labels):  # KMeansのラベルを使う
        f.write(f"{node} {community}\n")

print(f"ノードとそのクラスタは {output_file} に保存されました。")
