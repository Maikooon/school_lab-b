"""

入力
サーバごとのグラフの接続情報

出力



Nホップ目において、その時から自分のサーバに戻ってくる確率を計算
"""

import os
import numpy as np
from collections import defaultdict
import random
import matplotlib.pyplot as plt


def read_server_files(directory):
    """
    指定されたディレクトリ内のすべてのサーバファイルを読み取る。
    """
    adjacency_list = defaultdict(list)
    server_map = defaultdict(set)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                for line in f:
                    node_a, node_b, server_ip = line.strip().split(",")
                    node_a, node_b = int(node_a), int(node_b)

                    # 隣接リストを更新
                    adjacency_list[node_a].append(node_b)
                    adjacency_list[node_b].append(node_a)

                    # サーバマップを更新
                    server_map[server_ip].update([node_a, node_b])

    return adjacency_list, server_map


def run_random_walk(adjacency_list, server_map, initial_node, alpha, max_hops=1000):
    """
    ランダムウォークをシミュレートし、各サーバごとの滞在確率を計算する。
    """
    server_probabilities_over_hops = defaultdict(
        lambda: [0] * max_hops
    )  # 各サーバの確率をホップごとに記録
    current_node = initial_node
    hop = 0
    server_visits = defaultdict(int)  # サーバごとの訪問回数

    # ランダムウォークを開始
    while hop < max_hops:
        # 終了確率αで終了するか判定
        if random.random() < alpha:
            break

        # 隣接ノードへ等確率で遷移
        neighbors = adjacency_list[current_node]
        if not neighbors:
            break  # 隣接ノードがない場合、遷移を終了
        next_node = random.choice(neighbors)
        current_node = next_node
        hop += 1

        # 各サーバごとの訪問確率を計算
        for server, nodes in server_map.items():
            if current_node in nodes:
                server_visits[server] += 1

        # サーバごとの訪問確率を更新
        total_visits = (
            sum(server_visits.values()) if server_visits else 1
        )  # 訪問回数がゼロの場合は1で割る
        for server in server_map:
            server_probabilities_over_hops[server][hop] = (
                server_visits[server] / total_visits
            )

    return server_probabilities_over_hops, hop


def plot_server_probabilities(server_probabilities_over_hops, total_hops, alpha):
    """
    サーバごとの確率をホップ数に対してプロット
    """
    plt.figure(figsize=(10, 6))
    hops = range(total_hops)

    for server, probabilities in server_probabilities_over_hops.items():
        # 確率リストが max_hops より長い場合、total_hops に合わせる
        plt.plot(
            hops, probabilities[:total_hops], marker="o", label=f"Server: {server}"
        )

    # for server, probabilities in server_probabilities_over_hops.items():
    #     plt.plot(hops, probabilities, marker="o", label=f"Server: {server}")

    plt.title(f"Server Probabilities over Hops (α={alpha})")
    plt.xlabel("Hop Number")
    plt.ylabel("Probability")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 使用例
if __name__ == "__main__":
    # サーバ情報のディレクトリパス
    server_directory = (
        "./../server-data/test/"  # サーバごとに分かれたファイルが格納されたディレクトリ
    )

    # 終了確率の設定
    alpha = 0.01  # 終了確率 (例: 1%)

    # 隣接リストとサーバ情報を読み取る
    adjacency_list, server_map = read_server_files(server_directory)

    # 初期ノードの設定
    initial_node = 1

    # ランダムウォークを実行し、各サーバごとの確率を計算
    server_probabilities_over_hops, total_hops = run_random_walk(
        adjacency_list, server_map, initial_node, alpha
    )

    # 結果をプロット
    plot_server_probabilities(server_probabilities_over_hops, total_hops, alpha)
