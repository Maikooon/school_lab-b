"""
1で分割したコミュニティをさらに2つに分割することで、認可の際のグルーピングを再現する

サーバ内のグラフに対してコミュニティ分割を行う
METISで分割されたものを再びMETISで分割
サーバ内のグラフに対して、コミュニティ分割を行う。

この時、サーバ間で制御できるようにするために、コミュニティの名前を変更
変更前：サーバ内で一意
変更後：サーバ間で一意一度しか生成されない乱数にすることで実現


入力
- グラフのエッジファイル
- ノードのコミュニティ情報ファイル

出力
コミュニティごとに分割されるので、サーバごとのファイルにまとめる(合計６つのファイルが生成される)
- community_A.txt, community_B.txt _>server_abilene03_edges_community.txt


"""

import networkx as nx
import metis
import os

GRAPH = os.getenv("GRAPH", "fb-caltech-connected")


# エッジ情報をファイルから読み込む関数
def read_edges(file_path):
    edges = []
    with open(file_path, "r") as f:
        for line in f:
            node1, node2 = map(int, line.strip().split())
            edges.append((node1, node2))
    return edges


# ノードのコミュニティ情報をファイルから読み込む関数
def read_communities(file_path):
    communities = {}
    with open(file_path, "r") as f:
        for line in f:
            node, community = map(int, line.strip().split())
            communities[node] = community
    return communities


# グラフを構築する関数
def build_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


# コミュニティごとのサブグラフを分割
def split_community(community_nodes, G):
    subgraph = G.subgraph(community_nodes)

    # METISでサブグラフを2つに分割
    # 隣接リストと重み付きエッジのリストを作成
    adjacency = [list(subgraph.neighbors(n)) for n in subgraph.nodes]

    # METISの形式に従い、隣接ノードリストを構築
    _, parts = metis.part_graph(subgraph, 2)

    # 分割された結果のノードの新しいコミュニティ番号
    new_communities = {node: part for node, part in zip(subgraph.nodes, parts)}

    return new_communities


# ファイルからエッジとコミュニティ情報を読み込む
edges = read_edges("./../Louvain/graph/" + GRAPH + ".gr")
# node_communities = read_communities(
#     "./by-my-own-division/" + GRAPH + "/node_community.txt"
# )
node_communities = read_communities("./new/" + GRAPH + "/node_community.txt")

# グラフの作成
G = build_graph(edges)

# コミュニティごとにファイルに保存するマッピング
file_mapping = {
    0: (
        f"./new/{GRAPH}/community_A.txt",
        f"./new/{GRAPH}/community_B.txt",
    ),
    1: (
        f"./new/{GRAPH}/community_C.txt",
        f"./new/{GRAPH}/community_D.txt",
    ),
    2: (
        f"./new/{GRAPH}/community_E.txt",
        f"./new/{GRAPH}/community_F.txt",
    ),
}

# 各コミュニティを2つに分割し、結果をファイルに保存
new_community_assignments = {}
i = 0
for community_id in set(node_communities.values()):
    community_nodes = [
        n for n in node_communities if node_communities[n] == community_id
    ]
    split_result = split_community(community_nodes, G)

    # 新しいコミュニティ番号を割り当てる
    new_assignments = {
        node: community_id * 2 + part for node, part in split_result.items()
    }
    new_community_assignments.update(new_assignments)

    # ファイルに出力
    file_A, file_B = file_mapping[community_id]
    community_1 = ["0", "2", "4"]
    community_2 = ["1", "3", "5"]
    with open(file_A, "w") as f_A, open(file_B, "w") as f_B:
        for node, part in new_assignments.items():
            if part == community_id * 2:
                f_A.write(f"{node} {community_1[i]}\n")  # コミュニティA, C, E
            else:
                f_B.write(f"{node} {community_2[i]}\n")  # コミュニティB, D, F
        i += 1
        print(i)

print("コミュニティ分割完了。各コミュニティのノードがファイルに保存されました。")
