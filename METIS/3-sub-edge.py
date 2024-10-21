# """
# サーバ内のグラフを表現するエッジリストを作成
# server-0-edges-community.txt が出力
# """


# # ファイルの読み込み関数
# def read_file(file_path):
#     with open(file_path, "r") as file:
#         return file.readlines()


# GRAPGNAME = "karate"

# # コミュニティファイルのパス
# community_file_path = "./" + GRAPGNAME + "/node_community.txt"
# # エッジファイルのパス
# edge_file_path = "./../Louvain/graph/" + GRAPGNAME + ".gr"

# # コミュニティファイルを読み込み、辞書に変換
# community_data = {}
# community_lines = read_file(community_file_path)
# for line in community_lines:
#     node, community = map(int, line.split())
#     community_data[node] = community

# # エッジファイルを読み込み、コミュニティごとに分類
# community_edges = {}
# edge_lines = read_file(edge_file_path)
# for line in edge_lines:
#     node1, node2 = map(int, line.split())
#     comm1 = community_data.get(node1)
#     comm2 = community_data.get(node2)

#     # 両方のノードが同じコミュニティに属する場合のみ
#     if comm1 == comm2:
#         if comm1 not in community_edges:
#             community_edges[comm1] = []
#         community_edges[comm1].append((node1, node2))

# # 各コミュニティごとのエッジファイルを生成
# for community, edges in community_edges.items():
#     filename = "./" + GRAPGNAME + f"/server_{community}_edges.txt"
#     with open(filename, "w") as f:
#         for edge in edges:
#             f.write(f"{edge[0]} {edge[1]}\n")
#     print(f"コミュニティ {community} のエッジファイル {filename} を生成しました。")
