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
    save_node_community(parts, graph_name)


# ファイルからノードの接続情報を読み込む関数
def load_graph_from_file(filename):
    G = nx.Graph()  # 無向グラフの用意
    with open(filename, "r") as f:
        for line in f:
            u, v = map(int, line.split())  # ノードのペアを取得
            G.add_edge(u, v)  # エッジを追加
    return G


# ノードとコミュニティ情報をファイルに保存する関数
def save_node_community(parts, graph_name):
    output_file = f"./{graph_name}/node_community.txt"
    with open(output_file, "w") as f:
        for i, p in enumerate(parts):
            f.write(f"{i} {p}\n")


# メイン処理
if __name__ == "__main__":
    GRAPHNAME = "ca-grqc-connected"  # グラフの名前
    npart = 3  # 分割数を指定
    load_and_partition_graph(GRAPHNAME, npart)
