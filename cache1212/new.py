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


def run_random_walk_with_influx(
    adjacency_list, server_map, initial_node, alpha, max_hops=1000
):
    """
    ランダムウォークをシミュレートし、ホップごとのサーバへの流入確率を計算する。
    """
    server_influx_over_hops = defaultdict(
        lambda: [0] * max_hops
    )  # サーバごとの流入回数を記録
    current_node = initial_node
    current_server = None
    hop = 0

    # サーバ情報の逆マップを作成（ノード -> サーバ）
    node_to_server = {}
    for server, nodes in server_map.items():
        for node in nodes:
            node_to_server[node] = server

    # ランダムウォークを開始
    while hop < max_hops:
        # 終了確率alphaで終了するか判定
        if random.random() < alpha:
            break

        # 隣接ノードへ等確率で遷移
        neighbors = adjacency_list[current_node]
        if not neighbors:
            break  # 隣接ノードがない場合、遷移を終了
        next_node = random.choice(neighbors)

        # サーバの流入を記録
        next_server = node_to_server.get(next_node)
        if next_server and next_server != current_server:
            server_influx_over_hops[next_server][hop] += 1

        # 状態を更新
        current_node = next_node
        current_server = next_server
        hop += 1

    # 流入確率を計算
    server_influx_probabilities = defaultdict(list)
    for server, influx_counts in server_influx_over_hops.items():
        total_influx = sum(influx_counts)
        if total_influx > 0:
            server_influx_probabilities[server] = [
                count / total_influx for count in influx_counts
            ]

    return server_influx_probabilities, hop


def plot_server_influx_probabilities(server_influx_probabilities, total_hops, alpha):
    """
    サーバごとの流入確率をホップ数に対してプロット
    """
    plt.figure(figsize=(10, 6))
    hops = range(total_hops)

    for server, probabilities in server_influx_probabilities.items():
        plt.plot(
            hops, probabilities[:total_hops], marker="o", label=f"Server: {server}"
        )

    plt.title(f"Server Influx Probabilities over Hops (\u03b1={alpha})")
    plt.xlabel("Hop Number")
    plt.ylabel("Influx Probability")
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

    # ランダムウォークを実行し、各サーバごとの流入確率を計算
    server_influx_probabilities, total_hops = run_random_walk_with_influx(
        adjacency_list, server_map, initial_node, alpha
    )

    # 結果をプロット
    plot_server_influx_probabilities(server_influx_probabilities, total_hops, alpha)
