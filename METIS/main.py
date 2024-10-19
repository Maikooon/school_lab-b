import numpy as np
import networkx as nx  # グラフの作成のため
import metis  # グラフの分割のため
import os


# グラフを読み込んで、描画し、分割を行う関数
def load_and_partition_graph(graph_name, partition_count):
    # グラフのファイル名
    filename = f"./../Louvain/graph/{graph_name}.gr"
    # グラフの読み込み
    G = load_graph_from_file(filename)
    # 出力先のディレクトリを作成
    outdir = f"./{graph_name}"
    make_dir(outdir)
    # グラフを描画
    draw_graph(G, outdir, f"./file1.png")
    # グラフの分割
    edgecut, parts = metis.part_graph(G, partition_count)
    # ノードの色を分割に応じて設定
    set_node_colors(G, parts)
    # 再描画
    draw_graph(G, outdir, f"./file2.png")
    # ノードとコミュニティ情報をファイルに保存
    save_node_community(parts, outdir)


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
    for i, p in enumerate(parts):
        G.nodes[i]["color"] = colors[p]  # ノードの色を設定


# ノードとコミュニティ情報をファイルに保存する関数
def save_node_community(parts, outdir):
    with open(os.path.join(outdir, "node_community.txt"), "w") as f:
        for i, p in enumerate(parts):
            f.write(f"{i} {p}\n")


# メイン処理
if __name__ == "__main__":
    GRAPHNAME = "karate"  # グラフの名前
    npart = 3  # 分割数を指定
    load_and_partition_graph(GRAPHNAME, npart)
