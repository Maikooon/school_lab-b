import networkx as nx
import random

# エッジリストファイルとコミュニティファイルのパス
edges_file = 'a.txt'
communities_file = 'a.tcm'

# グラフの定義
G = nx.Graph()

# エッジリストの読み込み
with open(edges_file, 'r') as f:
    for line in f:
        if line.strip():  # 空行でないことを確認
            edge_data = line.strip().split()
            if len(edge_data) == 2:
                node1, node2 = map(int, edge_data)
                G.add_edge(node1, node2)
            else:
                raise ValueError("Each line in the edges file should contain two integers representing an edge.")

# ノードのコミュニティ辞書の作成
node_communities = {}
with open(communities_file, 'r') as f:
    for line in f:
        if line.strip():  # 空行でないことを確認
            node, community = map(int, line.strip().split())
            node_communities[node] = community

# αの確率
alpha = 0.85

def random_walk(graph, node_communities, start_node, alpha):
    current_node = start_node
    path = [current_node]
    
    while random.random() > alpha:
        neighbors = list(graph.neighbors(current_node))
        next_node = random.choice(neighbors)
        path.append(next_node)
        
        if node_communities[current_node] != node_communities[next_node]:
            print(f"Node {next_node} is in a different community from Node {current_node}")
        
        current_node = next_node
    
    return path

total = 0
for i in range(1, 32):
    # スタートノードを設定
    start_node = i

    # ランダムウォークの実行
    path = random_walk(G, node_communities, start_node, alpha)
    length = len(path)
    print(f"Random walk path: {path}")
    total += length

ave = total / 31
print(f"Average length: {ave}")
print(f"Total length: {total}")
