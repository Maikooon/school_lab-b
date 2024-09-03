import os

# コミュニティファイルのリスト
community_file_list = [
    "ca-grqc-connected.cm",
    "cmu.cm",
    # "com-amazon-connected.cm",
    # "email-enron-connected.cm",
    "fb-caltech-connected.cm",
    # "fb-pages-company.cm",
    "karate-graph.cm",
    "karate.cm",
    "rt-retweet.cm",
    "simple_graph.cm",
    # "soc-slashdot.cm",
    "tmp.cm",
]


def select_graph():
    # ユーザーに選択肢を表示
    print("グラフファイルを選択してください:")
    for i, file_name in enumerate(community_file_list):
        print(f"{i}: {file_name}")

    # ユーザーからの入力を受け取る
    try:
        choice = int(input("番号を入力してください: "))
        if choice < 0 or choice >= len(community_file_list):
            raise ValueError("無効な番号が入力されました。")
        return community_file_list[choice]
    except ValueError as e:
        print(f"エラー: {e}")
        return None


def process_communities(graph_file_name):
    input_file_path = os.path.join(
        "../../../calc-modularity/new_community", graph_file_name
    )

    # コミュニティごとにノードを格納するためのリストを初期化
    community_list = []

    # ファイルを読み込み、コミュニティごとにノードを分類
    with open(input_file_path, "r") as f:
        for line in f:
            node, community = map(int, line.split())
            # 必要ならば、リストを拡張して格納
            while len(community_list) <= community:
                community_list.append([])
            community_list[community].append(node)

    # 各コミュニティに対して処理を行う
    for community, key_nodes in enumerate(community_list):
        if not key_nodes:
            continue

        # 全ノードとそのコミュニティをリストに格納
        node_community_list = []
        with open(input_file_path, "r") as f:
            for line in f:
                node, community_num = map(int, line.split())
                node_community_list.append((node, community_num))

        # 結果を二重リスト形式で格納
        result_list = []
        for key_node in key_nodes:
            key_community = next(
                community for node, community in node_community_list if node == key_node
            )
            # 自分と同じコミュニティのノードと自身を除くノードをリストに格納
            value_nodes = [
                node
                for node, community_num in node_community_list
                if node != key_node and community_num != key_community
            ]
            result_list.append([key_node, value_nodes])

        # 指定の形式に変換する
        formatted_list = []
        for key_node, value_nodes in result_list:
            formatted_string = f"{key_node}: " + ", ".join(map(str, value_nodes))
            formatted_list.append(formatted_string)

        # 結果をファイルに書き出し
        graph_name = os.path.splitext(graph_file_name)[0]
        output_dir = os.path.join("./new-community-table/", graph_name)
        os.makedirs(output_dir, exist_ok=True)  # 出力ディレクトリが存在しない場合は作成
        output_file_path = os.path.join(output_dir, f"community_{community}_result.txt")
        with open(output_file_path, "w") as out_file:
            for result in formatted_list:
                out_file.write(f"{result},\n")
        print(
            f"コミュニティ {community} の結果を {output_file_path} に書き出しました。"
        )


def main():
    # グラフを選択
    selected_graph = select_graph()

    if selected_graph:
        print(f"選択されたグラフ: {selected_graph}")
        process_communities(selected_graph)
    else:
        print("グラフが選択されませんでした。")


if __name__ == "__main__":
    main()
