import numpy as np
import networkx as nx  # グラフの作成のため
import metis  # グラフの分割のため
import os


# グラフを読み込んで、分割を行う関数
def load_and_partition_graph(graph_name, partition_count):
    # グラフのファイル名
    filename = f"./../Louvain/graph/{graph_name}.gr"
    # グラフの読み込み
    G = load_graph_from_file(filename)
    # ノードの分割を行う
    edgecut, parts = metis.part_graph(G, partition_count)
    # ノードとコミュニティ情報をファイルに保存
    save_node_community(parts, graph_name, partition_count)


# ファイルからノードの接続情報を読み込む関数
def load_graph_from_file(filename):
    G = nx.Graph()  # 無向グラフの用意
    with open(filename, "r") as f:
        for line in f:
            u, v = map(int, line.split())  # ノードのペアを取得
            G.add_edge(u, v)  # エッジを追加
    return G


# ノードとコミュニティ情報をファイルに保存する関数
def save_node_community(parts, graph_name, partition_count):
    output_file = f"./{graph_name}/{partition_count}/node_community.txt"
    # フォルダがなければ作成
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # ファイルがなければ作成
    if not os.path.isfile(output_file):
        with open(output_file, "w") as file:
            # 初期データを書き込む場合
            file.write("Your initial content here\n")

    print(f"File '{output_file}' is ready.")
    with open(output_file, "w") as f:
        for i, p in enumerate(parts):
            f.write(f"{i} {p}\n")


# TODO:グラフの名前を定義するーメイン処理
# if __name__ == "__main__":
#     GRAPH = os.getenv("GRAPH", "com-amazon-connected")
#     npart = 15  # 分割数を指定
#     load_and_partition_graph(GRAPH, npart)
if __name__ == "__main__":
    GRAPH = os.getenv("GRAPH", "ca-grqc-connected")
    partitions = [
        2,
        3,
        5,
        8,
        10,
        15,
        20,
        25,
        30,
        35,
        40,
        45,
        50,
        55,
        60,
        65,
        70,
        75,
        80,
        85,
        90,
        95,
        100,
    ]  # 分割数を配列で指定

    for npart in partitions:
        load_and_partition_graph(GRAPH, npart)
