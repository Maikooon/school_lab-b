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
具体的には、何ホップ目までに遷移しているのかがわかる\
    
何とkなくの結果出る
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


def run_random_walk_with_return(adjacency_list, node_to_server, start_node, alpha):
    """
    始点ノードからランダムウォークをシミュレートし、外部サーバから指定サーバへの流入確率を累積的に計算する。
    """
    # サーバごとの流入回数を記録（ホップ数を無制限に記録）
    server_return_counts = defaultdict(list)

    # 始点ノードからランダムウォークを実行
    current_node = start_node
    hop = 0
    initial_server = node_to_server.get(start_node)  # 始点ノードのサーバ
    print("init server", initial_server)

    if initial_server is None:
        print(f"エラー: 始点ノード {start_node} はサーバに関連付けられていません。")
        return None

    while True:
        # 現在のノードのサーバを取得
        current_server = node_to_server.get(current_node)

        # 次に移動するサーバを決定する
        # print("start_server", current_server)

        # 外部サーバからの流入を記録（サーバが異なる場合のみカウント）
        if current_server is not None and current_server != initial_server:
            if current_server not in server_return_counts:
                server_return_counts[current_server] = []
            if len(server_return_counts[current_server]) <= hop:
                server_return_counts[current_server].extend(
                    [0] * (hop - len(server_return_counts[current_server]) + 1)
                )
            server_return_counts[current_server][hop] += 1

        # 終了確率 alpha で終了するか判定
        if random.random() < alpha:
            print("break")
            break

        # 隣接ノードへ等確率で遷移
        neighbors = adjacency_list.get(current_node, [])
        if not neighbors:
            print("-" * 10)
            break  # 隣接ノードがない場合、遷移を終了するが、おそらく到達し得ない
        current_node = random.choice(neighbors)
        hop += 1

    # 流入確率を計算（累積確率）
    server_return_probabilities = {}
    # ここを複数回実行することによって集める、累積は集まった配列をすべて足し合わせて、それを配列の数(つまりRwer数)で割ることによって求める
    # そのため、以下のようなHop単位の累積の計算のしかたは行わない？

    print("ここには回数が入っている？", server_return_counts)
    for server, counts in server_return_counts.items():
        cumulative_counts = np.cumsum(counts)  # 累積カウント
        # このように計算した時の確立の１は何？？
        total_walks = sum(cumulative_counts) if sum(cumulative_counts) > 0 else 1
        probabilities = [count / total_walks for count in cumulative_counts]
        server_return_probabilities[server] = probabilities

    # 結果を返す
    return server_return_probabilities


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
    server_directory = (
        "./../server-data/test/"  # サーバごとに分かれたファイルが格納されたディレクトリ
    )

    # 終了確率の設定
    alpha = 0.15  # 終了確率 (例: 1%)

    # 隣接リストとサーバ情報を読み取る
    adjacency_list, node_to_server = read_server_files(server_directory)

    # 始点ノードを指定（例：ノード2から開始）
    start_node = 1

    # ランダムウォークを実行し、Nホップ以内に各サーバへ流入する累積確率を計算
    server_return_probabilities = run_random_walk_with_return(
        adjacency_list, node_to_server, start_node, alpha
    )

    # 結果をプロット
    plot_return_probabilities(server_return_probabilities, alpha)
