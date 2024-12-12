import os
import numpy as np
from collections import defaultdict
import random
import matplotlib.pyplot as plt


"""
2123
読み取りとサーバ移動がうまく行った
いえい

Hop単位の累積の計算方法求める
具体的には、何ホップ目までに遷移しているのかがわかる

どのサーバにいるかのみがわかる
"""


def read_server_files(directory):
    """
    指定されたディレクトリ内のすべてのサーバファイルを読み取る。
    """
    adjacency_list = defaultdict(list)
    server_map = defaultdict(set)

    # 各ノードがどのサーバに属するかを記録する
    node_to_server = {}

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

                    # サーバマップを更新（エッジの両端のノードをそのサーバに追加）
                    server_map[server_ip].update([node_a, node_b])

                    # ノードの所属サーバを記録
                    node_to_server[node_a] = server_ip
                    node_to_server[node_b] = server_ip

    # print(adjacency_list)
    # print(server_map)
    # print(node_to_server)
    return adjacency_list, node_to_server


import random
import numpy as np
from collections import defaultdict


def run_random_walk_with_return(
    adjacency_list, node_to_server, start_node, alpha, num_walks=10
):
    """
    始点ノードからランダムウォークをシミュレートし、外部サーバから指定サーバへの流入確率を累積的に計算する。
    複数回のランダムウォーク結果を累積的に収集し、流入確率を求める。


    TODO'改変アルゴリズム
    初回に移動したHop数目だけ獲得啜る、具体的には、２つのRwerがあり３Hop目に達したRwerと５Hop目に達したRwerがある場合、それぞれのRwerの３Hop目と５Hop目の数を足し合わせて、それをRwerの数で割る
    この時では、５Hop目では１００％の確確率で自分のサーバに戻ってくるが、３Hop目では５０％の確率で自分のサーバに戻ってくるということがわかる
    内部のノードも含めた場合には、じぶんのサーバに戻ってくる確率が限りなく低く0%ほどになる可能性もある

    """
    # サーバごとの流入回数を記録（ホップ数を無制限に記録）
    server_return_counts = defaultdict(
        lambda: defaultdict(int)
    )  # {サーバ: {ホップ数: 回数}}

    # ランダムウォークを複数回実行
    for _ in range(num_walks):
        current_node = start_node
        hop = 0
        initial_server = node_to_server.get(start_node)  # 始点ノードのサーバ

        if initial_server is None:
            print(f"エラー: 始点ノード {start_node} はサーバに関連付けられていません。")
            return None

        while True:
            # 現在のノードのサーバを取得
            current_server = node_to_server.get(current_node)
            print("current_server", current_server)

            # 外部サーバからの流入を記録（サーバが異なる場合のみカウント）
            if current_server is not None and current_server != initial_server:
                server_return_counts[current_server][hop] += 1

            # 終了確率 alpha で終了するか判定
            if random.random() < alpha:
                break

            # 隣接ノードへ等確率で遷移
            neighbors = adjacency_list.get(current_node, [])
            if not neighbors:
                break  # 隣接ノードがない場合、遷移を終了
            current_node = random.choice(neighbors)
            hop += 1

    # 流入確率を計算（累積確率）

    server_return_probabilities = {}

    for server, counts_per_hop in server_return_counts.items():
        print("それぞれのRWの長", counts_per_hop)
        max_hop = max(counts_per_hop.keys())  # 最大ホップ数
        print("max_hop", max_hop)
        cumulative_counts = np.zeros(max_hop + 1)  # 累積カウントの初期化

        # ホップ数ごとの累積計算
        for hop, count in counts_per_hop.items():
            cumulative_counts[hop] = count

        total_walks = num_walks  # ランダムウォークの回数
        print("total_walks", total_walks)
        probabilities = cumulative_counts / total_walks  # 累積確率を計算

        server_return_probabilities[server] = probabilities

    # 結果を返す
    return server_return_probabilities


# 結果のプロット
import matplotlib.pyplot as plt


def plot_return_probabilities(server_return_probabilities, alpha):
    """
    各サーバへの累積流入確率をプロット。
    """
    plt.figure(figsize=(10, 6))

    for server, probabilities in server_return_probabilities.items():
        hops = range(len(probabilities))
        plt.plot(hops, probabilities, marker="o", label=f"Server: {server}")

    plt.title(f"Server Cumulative Influx Probabilities (α={alpha})")
    plt.xlabel("Hop Number")
    plt.ylabel("Cumulative Probability")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 使用例
if __name__ == "__main__":
    # サーバ情報のディレクトリパス
    server_directory = "./../server-data/test2/"  # サーバごとに分かれたファイルが格納されたディレクトリ

    # 終了確率の設定
    alpha = 0.1  # 終了確率 (例: 1%)

    # 隣接リストとサーバ情報を読み取る
    adjacency_list, node_to_server = read_server_files(server_directory)

    # 始点ノードを指定（例：ノード1から開始）
    start_node = 2

    # ランダムウォークを実行し、各サーバへの流入確率を計算
    server_return_probabilities = run_random_walk_with_return(
        adjacency_list, node_to_server, start_node, alpha
    )

    # 結果をプロット
    plot_return_probabilities(server_return_probabilities, alpha)
