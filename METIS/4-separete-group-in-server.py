"""

新しくなったのでこの実行の必要性なくなった？
"""

import numpy as np
import networkx as nx
import metis
import os

# グラフファイルのリストを定義 (複数のグラフ名や番号)
graph_files = [
    {"GRAPHNAME": "karate", "NUMBER": "0"},
    {"GRAPHNAME": "karate", "NUMBER": "1"},
    {"GRAPHNAME": "karate", "NUMBER": "2"},
]
npart = 2  # 分割数を指定

# 各ファイル間でコミュニティ番号を一意にするためのグローバルカウンタ
global_community_counter = 0


# 各グラフファイルに対して処理を行う
def process_multiple_graphs(graph_file_list, npart):
    global global_community_counter  # グローバルカウンタを使用

    for graph_file in graph_file_list:
        GRAPHNAME = graph_file["GRAPHNAME"]
        NUMBER = graph_file["NUMBER"]

        GRAPH_FILE = "./" + GRAPHNAME + "/server_" + NUMBER + "_edges.txt"
        OUTPUT_DIR = "./" + GRAPHNAME + "/group"  # 出力先のディレクトリ

        print(f"Processing graph: {GRAPHNAME}, NUMBER: {NUMBER}")
        global_community_counter = load_and_partition_graph(
            GRAPH_FILE, OUTPUT_DIR, npart, GRAPHNAME, NUMBER, global_community_counter
        )


# グラフを読み込んで、描画し、分割を行う関数
def load_and_partition_graph(
    graph_file, output_dir, partition_count, graph_name, number, community_counter
):
    # グラフの読み込み
    G = load_graph_from_file(graph_file)
    make_dir(output_dir)

    # グラフを描画
    draw_graph(G, output_dir, f"{graph_name}_{number}_file1.png")

    # グラフの分割
    edgecut, parts = metis.part_graph(G, partition_count)

    # グローバルカウンタを使用して、コミュニティ番号を一意に設定
    parts_with_global_ids = [p + community_counter for p in parts]

    # 次のファイルのためにカウンタを更新
    new_community_counter = community_counter + partition_count

    # ノードの色を分割に応じて設定
    set_node_colors(G, parts_with_global_ids)

    # 再描画
    draw_graph(G, output_dir, f"{graph_name}_{number}_file2.png")

    # ノードとコミュニティ情報をファイルに保存
    save_node_community(G, parts_with_global_ids, output_dir, graph_name, number)

    return new_community_counter  # 更新されたカウンタを返す


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
        G.nodes[node]["color"] = colors[p % len(colors)]  # ノードの色を設定


# ノードとコミュニティ情報をファイルに保存する関数
def save_node_community(G, parts, outdir, graph_name, number):
    node_list = list(G.nodes)

    # コミュニティ情報を保存するファイル名
    output_file = os.path.join(f"./{graph_name}/server_{number}_edges_community.txt")

    with open(output_file, "w") as f:
        for i, p in enumerate(parts):
            node = node_list[i]
            f.write(f"{node} {p}\n")


# メイン処理
if __name__ == "__main__":
    process_multiple_graphs(graph_files, npart)
