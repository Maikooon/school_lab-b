# ファイルからデータを読み込み
community_file = "./../../Louvain/community/karate.tcm"
edge_file = "./../../Louvain/graph/karate.gr"

# コミュニティごとのIPアドレスのマッピング
ip_mapping = {0: "10.58.60.3", 1: "10.58.60.6", 2: "10.58.60.11", 3: "10.58.60.5"}


# コミュニティ情報の読み込み
def read_communities(file_path):
    communities = {}
    with open(file_path, "r") as f:
        for line in f:
            node, community = map(int, line.split())
            if community not in communities:
                communities[community] = []
            communities[community].append(node)
    return communities


# エッジ情報の読み込み
def read_edges(file_path):
    edges = []
    with open(file_path, "r") as f:
        for line in f:
            node1, node2 = map(int, line.split())
            edges.append((node1, node2))
    return edges


# IP付きのグラフを生成し、コミュニティごとにファイルに出力
def generate_and_save_ip_graph(communities, edges):
    ip_graph = {}

    # コミュニティの初期化
    for community_id in communities.keys():
        ip_graph[community_id] = []

    # コミュニティ内の接続を追加
    for community_id, nodes in communities.items():
        for node1 in nodes:
            for node2 in nodes:
                if node1 != node2 and (
                    (node1, node2) in edges or (node2, node1) in edges
                ):
                    ip_graph[community_id].append(
                        f"{node1},{node2},{ip_mapping[community_id]}"
                    )

    # コミュニティ間の接続を追加
    for node1, node2 in edges:
        community1 = next(c for c, n in communities.items() if node1 in n)
        community2 = next(c for c, n in communities.items() if node2 in n)

        # コミュニティが異なる場合
        if community1 != community2:
            ip_graph[community1].append(f"{node1},{node2},{ip_mapping[community2]}")
            ip_graph[community2].append(f"{node2},{node1},{ip_mapping[community1]}")

    # コミュニティごとにファイルを書き込む
    for community_id, edges in ip_graph.items():
        file_name = f"community_{community_id}.txt"  # コミュニティごとのファイル名
        with open(file_name, "w") as f:
            for edge in edges:
                f.write(f"{edge}\n")  # エッジ情報をファイルに書き込み

    print("各コミュニティのファイルが生成されました。")


communities = read_communities(community_file)
edges = read_edges(edge_file)

# IP付きのグラフを生成し、ファイルに保存
generate_and_save_ip_graph(communities, edges)
