community_nodes = [
    [1, 2, 5, 10, 11, 14, 18, 21, 24, 25, 27, 31],
    [7, 8, 9, 12, 13, 16, 17, 20, 26, 28, 30],
    [0, 3, 4, 6, 15, 19, 22, 23, 29, 32, 33],
]

# ノード: 属しているコミュニティ形式に変換
node_community = []

for community_index, community in enumerate(community_nodes):
    for node in community:
        node_community.append(f"{node} {community_index}")

# 結果を出力
for line in node_community:
    print(line)


# ファイルに保存する
output_file_path = "./community_karate.txt"
with open(output_file_path, "w") as output_file:
    for line in node_community:
        output_file.write(f"{line}\n")
