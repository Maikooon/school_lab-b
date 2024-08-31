import json
import os

# コミュニティファイルのリスト
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


def process_communities(graph_file_name):
    input_file_path = os.path.join("../../../Louvain/community", graph_file_name)

    # コミュニティごとにノードを格納するための辞書を初期化
    community_dict = {}

    # ファイルを読み込み、コミュニティごとにノードを分類
    with open(input_file_path, "r") as f:
        for line in f:
            node, community = map(int, line.split())
            if community not in community_dict:
                community_dict[community] = []
            community_dict[community].append(node)

    # 各コミュニティに対して処理を行う
    for community, key_nodes in community_dict.items():
        # 全ノードとそのコミュニティを辞書に格納
        node_community_dict = {}
        with open(input_file_path, "r") as f:
            for line in f:
                node, community_num = map(int, line.split())
                node_community_dict[node] = community_num

        # 辞書を初期化し、キーに対する値を設定
        result_dict = {}
        for key_node in key_nodes:
            key_community = node_community_dict[key_node]
            # 自分と同じコミュニティのノードと自身を除くノードをリストに格納
            value_nodes = [
                node
                for node, community_num in node_community_dict.items()
                if node != key_node and community_num != key_community
            ]
            result_dict[key_node] = value_nodes

        # 結果を辞書型でファイルに書き出し
        graph_name = os.path.splitext(graph_file_name)[0]
        output_dir = os.path.join("./table", graph_name)
        os.makedirs(output_dir, exist_ok=True)  # 出力ディレクトリが存在しない場合は作成
        output_file_path = os.path.join(
            output_dir, f"community_{community}_result.json"
        )
        with open(output_file_path, "w") as out_file:
            json.dump(result_dict, out_file, indent=4)
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
