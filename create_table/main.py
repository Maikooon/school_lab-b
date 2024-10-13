# import json
# import os


# # 標準入力から得た番号を入力することで、対応するグラフを選択
# community_file_list = [
#         "ca-grqc-connected.cm",
#         "cmu.cm",
#         "com-amazon-connected.cm",
#         "email-enron-connected.cm",
#         "fb-caltech-connected.cm",
#         "fb-pages-company.cm",
#         "karate-graph.cm",
#         "karate.tcm",
#         "rt-retweet.cm",
#         "simple_graph.cm",
#         "soc-slashdot.cm",
#         "tmp.cm" ]

# # 分析するグラフを選択
# GRAPH = 'karate.tcm'
# # 元のファイルパスを指定
# input_file_path = '../../../Louvain/community/' + GRAPH

# # コミュニティごとにノードを格納するための辞書を初期化
# community_dict = {}

# # ファイルを読み込み、コミュニティごとにノードを分類
# with open(input_file_path, 'r') as f:
#     for line in f:
#         node, community = map(int, line.split())
#         if community not in community_dict:
#             community_dict[community] = []
#         community_dict[community].append(node)

# # 各コミュニティに対して処理を行う
# for community, key_nodes in community_dict.items():
#     # 全ノードとそのコミュニティを辞書に格納
#     node_community_dict = {}
#     with open(input_file_path, 'r') as f:
#         for line in f:
#             node, community_num = map(int, line.split())
#             node_community_dict[node] = community_num

#     # 辞書を初期化し、キーに対する値を設定
#     result_dict = {}
#     for key_node in key_nodes:
#         key_community = node_community_dict[key_node]
#         # 自分と同じコミュニティのノードと自身を除くノードをリストに格納
#         value_nodes = [node for node, community_num in node_community_dict.items()
#                        if node != key_node and community_num != key_community]
#         result_dict[key_node] = value_nodes

#     # 結果を辞書型でファイルに書き出し
#      # 拡張子を取り除いたファイル名を取得
#     graph_name = os.path.splitext(GRAPH)[0]
#     output_file_path = './table/' + graph_name + f'/community_{community}_result.json'
#     with open(output_file_path, 'w') as out_file:
#         json.dump(result_dict, out_file, indent=4)

#     print(f"コミュニティ {community} に対する辞書を作成し、JSON形式でファイルに書き出しました。")


import os

# グラフファイルのリスト
community_file_list = [
    "ca-grqc-connected.cm",
    "cmu.cm",
    "com-amazon-connected.cm",
    "email-enron-connected.cm",
    "fb-caltech-connected.cm",
    "fb-pages-company.cm",
    "karate-graph.cm",
    "karate.tcm",
    "rt-retweet.cm",
    "simple_graph.cm",
    "soc-slashdot.cm",
    "tmp.cm",
]


def load_nodes_communities(file_path):
    nodes_communities = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                node, community = map(int, line.split())
                nodes_communities.append((node, community))
    except FileNotFoundError:
        print(f"ファイルを開けません: {file_path}")
    return nodes_communities


def write_nodes_to_files(community_nodes, base_file_name):
    for community, nodes in community_nodes.items():
        file_name = "./table/" + base_file_name + f"/community_{community}.txt"
        try:
            with open(file_name, "w") as file:
                for node in nodes:
                    file.write(f"{node}\n")
        except IOError:
            print(f"ファイルを開けません: {file_name}")


def main():
    # ユーザーに選択肢を表示
    print("グラフファイルを選択してください:")
    for i, file_name in enumerate(community_file_list):
        print(f"{i}: {file_name}")

    # ユーザーからの入力を受け取る
    try:
        choice = int(input("番号を入力してください: "))
        if choice < 0 or choice >= len(community_file_list):
            raise ValueError("無効な番号が入力されました。")
        input_file_name = community_file_list[choice]
    except ValueError as e:
        print(f"エラー: {e}")
        return

    input_file_path = os.path.join("../../../Louvain/community", input_file_name)

    # 拡張子を取り除いたファイル名を取得
    base_file_name = os.path.splitext(input_file_name)[0]

    # ノードとコミュニティ情報を読み込む
    nodes_communities = load_nodes_communities(input_file_path)

    # コミュニティごとにノードを格納するための辞書
    community_nodes_map = {}
    for node, community in nodes_communities:
        if community not in community_nodes_map:
            community_nodes_map[community] = []
        community_nodes_map[community].append(node)

    # コミュニティごとにノードをファイルに書き込む
    write_nodes_to_files(community_nodes_map, base_file_name)


if __name__ == "__main__":
    main()
