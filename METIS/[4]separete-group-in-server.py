"""
サーバ内のグラフに対してコミュニティ分割を行う
METISで分割されたものを再びMETISで分割
サーバ内のグラフに対して、コミュニティ分割を行う。

この時、サーバ間で制御できるようにするために、コミュニティの名前を変更
変更前：サーバ内で一意
変更後：サーバ間で一意  一度しか生成されない乱数にすることで実現

生成されるファイル
/server_" + NUMBER + "_edges_community.txt
"""

import numpy as np
import networkx as nx  # グラフの作成のため
import metis  # グラフの分割のため
import os

NUMBER = "0"
GRAPHNAME = "karate"  # グラフの名前
npart = 2  # 分割数を指定
GRAPH_FILE = "./" + GRAPHNAME + "/server_" + NUMBER + "_edges.txt"
OUTPUT_DIR = "./" + GRAPHNAME + "/group"  # 出力先のディレクトリ


# グラフを読み込んで、描画し、分割を行う関数
def load_and_partition_graph(graph_name, partition_count):
    # グラフの読み込み
    G = load_graph_from_file(GRAPH_FILE)
    make_dir(OUTPUT_DIR)

    # グラフを描画
    draw_graph(G, OUTPUT_DIR, f"file1.png")

    # グラフの分割
    edgecut, parts = metis.part_graph(G, partition_count)

    # ノードの色を分割に応じて設定
    set_node_colors(G, parts)

    # 再描画
    draw_graph(G, OUTPUT_DIR, f"file2.png")

    # ノードとコミュニティ情報をファイルに保存
    save_node_community(G, parts, OUTPUT_DIR)


# ファイルからノードの接続情報を読み込む関数
def load_graph_from_file(filename):
    G = nx.Graph()  # 無向グラフの用意
    with open(filename, "r") as f:
        for line in f:
            u, v = map(int, line.split())  # ノードのペアを取得
            G.add_edge(u, v)  # エッジを追加
    return G


# 出力先のディレクトリを作成する関数
def make_dir(outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)


# グラフを描画する関数
def draw_graph(G, outdir, filename):
    g = nx.nx_agraph.to_agraph(G)
    g.draw(os.path.join(outdir, filename), prog="circo")


# ノードの色を分割に応じて設定する関数
def set_node_colors(G, parts):
    colors = ["#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF"]

    # ノードとパーティションの対応付け
    node_list = list(G.nodes)

    for i, p in enumerate(parts):
        node = node_list[i]  # parts の i 番目のインデックスに対応するノード
        print(f"Node {node} is in partition {p}")
        G.nodes[node]["color"] = colors[p]  # ノードの色を設定


# ノードとコミュニティ情報をファイルに保存する関数
def save_node_community(G, parts, outdir):
    node_list = list(G.nodes)
    with open(
        os.path.join("./" + GRAPHNAME + "/server_" + NUMBER + "_edges_community.txt"),
        "w",
    ) as f:
        for i, p in enumerate(parts):
            node = node_list[i]
            f.write(f"{node} {p}\n")


# メイン処理
if __name__ == "__main__":
    load_and_partition_graph(GRAPHNAME, npart)
