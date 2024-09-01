"""
新たなコミュニティを作成するプログラム

"""

import networkx as nx
from sklearn.cluster import FuzzyCMeans

# グラフの作成（例）
G = nx.Graph()
# ... エッジの追加

# Fuzzy C-means
fcm = FuzzyCMeans(n_clusters=4, random_state=0).fit(nx.adjacency_matrix(G).todense())
u, c, u0, d, jm, p, fpc = fcm.fit_predict(nx.adjacency_matrix(G).todense())

# 結果の表示
for i, node in enumerate(G.nodes):
    for j in range(4):
        print(f"Node {node}: Community {j} (membership: {u[i][j]})")
