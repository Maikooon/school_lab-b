import matplotlib.pyplot as plt
import networkx as nx


GRAPH = "fb-caltech-connected"


# エッジ情報をファイルから読み込む
# エッジ情報をファイルから読み込む（カンマ区切り）
def load_edges(file_paths):
    edges = []
    for file_path in file_paths:
        with open(file_path, "r") as file:
            for line in file:
                # 行をカンマで分割し、ノード1、ノード2、IPアドレスを抽出
                node1, node2, ip = line.strip().split(",")
                edges.append((int(node1), int(node2), ip))
    return edges


# コミュニティ情報をファイルから読み込む
def load_communities(file_path):
    community_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            node, community = line.split()
            community_dict[int(node)] = int(community)
    return community_dict


# 複数のエッジ情報ファイルを指定
edge_files = [
    "./" + GRAPH + "/community_0.txt",
    "./" + GRAPH + "/community_1.txt",
    "./" + GRAPH + "/community_2.txt",
    # 他のファイルも追加可能
]

# コミュニティ情報ファイルを指定
community_file = "./" + GRAPH + "/node_community.txt"

# エッジとコミュニティ情報を読み込む
edges = load_edges(edge_files)  # 複数のエッジ情報ファイルを読み込む
community_dict = load_communities(community_file)  # コミュニティ情報ファイルを読み込む

# グラフを作成
G = nx.Graph()

# エッジを追加（IPアドレスもエッジラベルとして使用）
for node1, node2, ip in edges:
    G.add_edge(node1, node2, label=ip)

# 描画
pos = nx.spring_layout(G, seed=42)  # ノードの配置

# ノードのコミュニティごとの色を決める（色分け）
community_colors = {0: "skyblue", 1: "lightgreen", 2: "lightcoral"}
node_colors = [community_colors[community_dict.get(node, -1)] for node in G.nodes]

# ノードとエッジの描画
plt.figure(figsize=(10, 10))
nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors, alpha=0.7)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7, edge_color="gray")

# エッジラベル（IPアドレス）を描画
edge_labels = nx.get_edge_attributes(G, "label")
edge_label_dict = {(node1, node2): f"{ip}" for node1, node2, ip in edges}
nx.draw_networkx_edge_labels(G, pos, font_size=6, edge_labels=edge_label_dict)

# ノードラベルの描画
nx.draw_networkx_labels(G, pos, font_size=6, font_color="black")
# ラベルは、IPだけでいい


# 図の表示
plt.title("Network Graph with IP Addresses")
plt.axis("off")
plt.savefig("./" + GRAPH + "/karate_graph.png")
plt.show()
