import json

graph_file_list = [
    "ca-grqc-connected.gr",
    "cmu.gr",
    "com-amazon-connected.gr",
    "fb-caltech-connected.gr",
    "karate-graph.gr",
    "karate.gr",
    "rt-retweet.gr",
    "simple_graph.gr",
    "soc-slashdot.gr",
    "tmp.gr",
]

FILE = "./../Louvain/graph/" + graph_file_list[1]
OUTPUT = graph_file_list[1][:-2] + ".json"
print(OUTPUT)


def create_json_from_file(filename):
    """
    ノードの繋がりからJSONを作成する関数。
    各ノードについて、グラフ内の全てのノードをランダムウォーカーとして設定。

    Args:
        filename: 入力ファイル名

    Returns:
        作成されたJSON文字列
    """

    # グラフの全ノードを一度に取得するための集合
    all_nodes = set()
    # 各ノードに接続しているノードを格納する辞書
    neighbors = {}

    with open(filename, "r") as f:
        for line in f:
            node1, node2 = map(int, line.strip().split())
            all_nodes.add(node1)
            all_nodes.add(node2)
            neighbors.setdefault(node1, set()).add(node2)
            neighbors.setdefault(node2, set()).add(node1)

    # 全てのノードペアに対してJSONを作成
    data = []
    for node1 in all_nodes:
        for node2 in all_nodes:
            if node1 != node2:
                data.append(
                    {
                        f"{node1}-{node2}": {
                            "0": list(
                                neighbors.get(node1, set()) - {node2}
                            ),  # 方向0のランダムウォーカー (node1から出ている辺)
                            "1": list(
                                neighbors.get(node2, set()) - {node1}
                            ),  # 方向1のランダムウォーカー (node2から出ている辺)
                        }
                    }
                )

    return json.dumps(data, indent=2)


if __name__ == "__main__":
    json_data = create_json_from_file(FILE)
    save_folder = "./allowTable/"
    output_path = os.path.join(save_folder, OUTPUT)
    with open(OUTPUT, "w") as f:
        f.write(json_data)
