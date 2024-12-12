import os
import numpy as np
from collections import defaultdict
import random
import matplotlib.pyplot as plt

import random
from collections import defaultdict
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


# def run_random_walk_with_return(adjacency_list, server_map, alpha, max_hops=1000):
#     """
#     ランダムウォークをシミュレートし、Nホップ以内に元のサーバに戻ってくる確率を計算する。
#     """
#     # サーバ情報の逆マップを作成（ノード -> サーバ）
#     node_to_server = {}
#     for server, nodes in server_map.items():
#         for node in nodes:
#             node_to_server[node] = server

#     # サーバごとの戻り確率を記録
#     server_return_counts = {server: [0] * max_hops for server in server_map}

#     # 各ノードからランダムウォークを実行
#     for initial_node in node_to_server:
#         current_node = initial_node
#         initial_server = node_to_server[initial_node]
#         hop = 0

#         # ランダムウォークを開始
#         while hop < max_hops:
#             # 現在のノードのサーバを取得
#             current_server = node_to_server.get(current_node)

#             # 元のサーバに戻った場合の処理
#             if current_server == initial_server:
#                 server_return_counts[initial_server][hop] += 1

#             # 終了確率alphaで終了するか判定
#             if random.random() < alpha:
#                 break

#             # 隣接ノードへ等確率で遷移
#             neighbors = adjacency_list[current_node]
#             if not neighbors:
#                 break  # 隣接ノードがない場合、遷移を終了
#             current_node = random.choice(neighbors)
#             hop += 1

#     # 元のサーバに戻る確率を計算
#     server_return_probabilities = {}
#     for server, counts in server_return_counts.items():
#         total_walks = (
#             sum(counts) if sum(counts) > 0 else 1
#         )  # 訪問回数がゼロの場合は1で割る
#         probabilities = [count / total_walks for count in counts]
#         server_return_probabilities[server] = probabilities

#     return server_return_probabilities


# def run_random_walk_with_return(adjacency_list, server_map, alpha, max_hops=1000):
#     """
#     ランダムウォークをシミュレートし、Nホップ以内に外部サーバから指定サーバへの流入確率を計算する。
#     """
#     # サーバ情報の逆マップを作成（ノード -> サーバ）
#     node_to_server = {}
#     for server, nodes in server_map.items():
#         for node in nodes:
#             node_to_server[node] = server

#     # サーバごとの流入回数を記録
#     server_return_counts = {server: [0] * max_hops for server in server_map}

#     # 各ノードからランダムウォークを実行
#     for initial_node in node_to_server:
#         current_node = initial_node
#         hop = 0
#         initial_server = node_to_server[initial_node]  # 開始ノードのサーバ

#         # ランダムウォークを開始
#         while hop < max_hops:
#             # 現在のノードのサーバを取得
#             current_server = node_to_server.get(current_node)

#             # 外部サーバからの流入を記録（サーバが異なる場合のみカウント）
#             if current_server is not None and current_server != initial_server:
#                 server_return_counts[current_server][hop] += 1

#             # 終了確率alphaで終了するか判定
#             if random.random() < alpha:
#                 break

#             # 隣接ノードへ等確率で遷移
#             neighbors = adjacency_list[current_node]
#             if not neighbors:
#                 break  # 隣接ノードがない場合、遷移を終了
#             current_node = random.choice(neighbors)
#             hop += 1

#     # 流入確率を計算（累積確率）
#     server_return_probabilities = {}
#     for server, counts in server_return_counts.items():
#         cumulative_counts = np.cumsum(counts)  # 累積カウント
#         total_walks = sum(cumulative_counts) if sum(cumulative_counts) > 0 else 1
#         probabilities = [count / total_walks for count in cumulative_counts]
#         server_return_probabilities[server] = probabilities

#     return server_return_probabilities


# def plot_return_probabilities(server_return_probabilities, total_hops, alpha):
#     """
#     Nホップ以内に各サーバへ流入する累積確率をプロット
#     """
#     plt.figure(figsize=(10, 6))
#     hops = range(total_hops)

#     for server, probabilities in server_return_probabilities.items():
#         plt.plot(
#             hops, probabilities[:total_hops], marker="o", label=f"Server: {server}"
#         )

#     plt.title(f"Server Cumulative Influx Probabilities within Hops (α={alpha})")
#     plt.xlabel("Hop Number")
#     plt.ylabel("Cumulative Probability")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()


# # 使用例
# if __name__ == "__main__":
#     # サーバ情報のディレクトリパス
#     server_directory = (
#         "./../server-data/test/"  # サーバごとに分かれたファイルが格納されたディレクトリ
#     )

#     # 終了確率の設定
#     alpha = 0.1  # 終了確率 (例: 1%)

#     # 隣接リストとサーバ情報を読み取る
#     adjacency_list, server_map = read_server_files(server_directory)

#     # ランダムウォークを実行し、Nホップ以内に各サーバへ流入する累積確率を計算
#     server_return_probabilities = run_random_walk_with_return(
#         adjacency_list, server_map, alpha
#     )

#     # 結果をプロット
#     total_hops = 100
#     plot_return_probabilities(server_return_probabilities, total_hops, alpha)


class RWer:
    def __init__(self, start_node, adjacency_list, node_to_server, alpha):
        """
        ランダムウォーカーの初期化
        """
        self.current_node = start_node  # 現在のノード
        self.adjacency_list = adjacency_list  # 隣接リスト
        self.node_to_server = node_to_server  # ノード -> サーバのマップ
        self.alpha = alpha  # 終了確率
        self.initial_server = node_to_server[start_node]  # 開始サーバ
        self.hop_count = 0  # 現在のホップ数
        self.terminated = False  # 終了フラグ

    def step(self):
        """
        ランダムウォークの1ステップを実行
        """
        if self.terminated:
            return None  # 終了している場合は何もしない

        # 終了確率で終了
        if random.random() < self.alpha:
            self.terminated = True
            return None

        # 隣接ノードが存在しない場合も終了
        neighbors = self.adjacency_list.get(self.current_node, [])
        if not neighbors:
            self.terminated = True
            return None

        # ランダムに隣接ノードを選択
        self.current_node = random.choice(neighbors)
        self.hop_count += 1
        return self.current_node

    def is_external_transition(self):
        """
        外部サーバへの遷移かどうかを判定
        """
        current_server = self.node_to_server.get(self.current_node)
        return current_server is not None and current_server != self.initial_server


def simulate_random_walk_from_node(
    start_node, adjacency_list, server_map, alpha, num_walkers
):
    """
    指定ノードからランダムウォークをシミュレートし、外部サーバへの累積流入確率を計算
    """
    # ノード -> サーバの逆マップ
    node_to_server = {
        node: server for server, nodes in server_map.items() for node in nodes
    }

    # 外部サーバへの流入回数を記録
    external_influx = [0] * (num_walkers + 1)

    # 各ランダムウォーカーをシミュレーション
    for _ in range(num_walkers):
        walker = RWer(start_node, adjacency_list, node_to_server, alpha)
        while not walker.terminated:
            walker.step()
            if walker.is_external_transition():
                external_influx[walker.hop_count] += 1

    # 累積確率を計算
    total_walks = num_walkers
    cumulative_probabilities = []
    cumulative_count = 0
    for count in external_influx:
        cumulative_count += count
        cumulative_probabilities.append(cumulative_count / total_walks)

    return cumulative_probabilities


def plot_cumulative_probabilities(cumulative_probabilities, alpha, start_node):
    """
    累積流入確率をプロット
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(cumulative_probabilities)), cumulative_probabilities, marker="o")
    plt.title(
        f"Cumulative External Influx Probabilities (α={alpha}, Start Node={start_node})"
    )
    plt.xlabel("Hop Count")
    plt.ylabel("Cumulative Probability")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 使用例
if __name__ == "__main__":
    # 隣接リストとサーバマップの例
    # adjacency_list = {
    #     "1": ["2", "3"],
    #     "2": ["1", "3", "5"],
    #     "3": ["1", "2"],
    #     "5": ["2"],
    # }

    # server_map = {"Server1": {"1", "2", "3"}, "Server2": {"5"}}
    adjacency_list, server_map = read_server_files("./../server-data/test/")

    # シミュレーションパラメータ
    start_node = "1"  # 開始ノード
    alpha = 0.1  # 終了確率
    num_walkers = 1000  # ランダムウォーカーの数

    # ランダムウォークを実行して累積確率を計算
    cumulative_probabilities = simulate_random_walk_from_node(
        start_node, adjacency_list, server_map, alpha, num_walkers
    )

    # 結果をプロット
    plot_cumulative_probabilities(cumulative_probabilities, alpha, start_node)
