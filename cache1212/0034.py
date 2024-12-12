import random
import numpy as np
from collections import defaultdict
import random
import numpy as np
from collections import defaultdict
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

改変する
スタバで最後にやってたやつ
"""

"""
始点ノードからランダムウォークをシミュレートし、外部サーバから指定サーバへの流入確率を累積的に計算する。
複数回のランダムウォーク結果を累積的に収集し、流入確率を求める。

始点ノードからランダムウォークをシミュレートし、
一旦外部に出た後、始点サーバに再び戻ってくる確率を計算する。


始点サーバのすべてのノードからの実行を実現
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
    print(node_to_server)
    return adjacency_list, node_to_server


def run_random_walk_with_return(
    adjacency_list, node_to_server, start_nodes, alpha, num_walks=10
):
    """
    指定されたサーバに属するすべてのノードからランダムウォークをシミュレートし、
    一旦外部に出た後、始点サーバに再び戻ってくる確率の平均を計算する。
    """
    # 始点サーバに戻る回数を記録
    total_return_counts = defaultdict(int)  # {ホップ数: 回数}

    for start_node in start_nodes:
        # 各ノードからの戻り回数を記録
        return_counts = defaultdict(int)  # {ホップ数: 回数}

        # ランダムウォークを複数回実行
        for _ in range(num_walks):
            current_node = start_node
            hop = 0
            initial_server = node_to_server.get(start_node)  # 始点ノードのサーバ

            if initial_server is None:
                print(
                    f"エラー: 始点ノード {start_node} はサーバに関連付けられていません。"
                )
                continue

            exited_initial_server = False  # 始点サーバを離れたかどうか

            while True:
                # 現在のノードのサーバを取得
                current_server = node_to_server.get(current_node)

                # 始点サーバに戻った場合の記録
                if exited_initial_server and current_server == initial_server:
                    return_counts[hop] += 1
                    break  # 戻ったら終了

                # 始点サーバを離れたことを確認
                if current_server != initial_server:
                    exited_initial_server = True

                # 終了確率 alpha で終了するか判定
                if random.random() < alpha:
                    break

                # 隣接ノードへ等確率で遷移
                neighbors = adjacency_list.get(current_node, [])
                if not neighbors:
                    break  # 隣接ノードがない場合、遷移を終了
                current_node = random.choice(neighbors)
                hop += 1

        # 各ノードの戻り回数を累積
        for hop, count in return_counts.items():
            total_return_counts[hop] += count

    # 始点サーバに戻る確率を計算
    max_hop = max(total_return_counts.keys()) if total_return_counts else 0
    return_probabilities = np.zeros(max_hop + 1)

    total_walks = len(start_nodes) * num_walks
    print("total_walks", total_walks)
    print(len(start_nodes))
    for hop, count in total_return_counts.items():
        return_probabilities[hop] = count / total_walks
        # こちらかと思ったが、それぞれの頂点から数回づつ行っているので上で正しい
        # return_probabilities[hop] = count / len(start_nodes)

    return return_probabilities


# 結果のプロット
import matplotlib.pyplot as plt


def plot_return_probabilities(return_probabilities, alpha):
    """
    始点サーバに再び戻る確率をプロット。
    """
    plt.figure(figsize=(10, 6))

    hops = range(len(return_probabilities))
    plt.plot(hops, return_probabilities, marker="o", label="Return Probabilities")

    plt.title(f"Return Probabilities to Start Server (α={alpha})")
    plt.xlabel("Hop Number")
    plt.ylabel("Return Probability")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 使用例
if __name__ == "__main__":
    # サーバ情報のディレクトリパス
    server_directory = "./../server-data/test2/"  # サーバごとに分かれたファイルが格納されたディレクトリ

    # 終了確率の設定
    alpha = 0.1  # 終了確率 (例: 10%)

    # 隣接リストとサーバ情報を読み取る
    adjacency_list, node_to_server = read_server_files(server_directory)

    # 始点サーバを指定（例：サーバAに属するノード）
    start_server = "10.1"
    start_nodes = [
        node for node, server in node_to_server.items() if server == start_server
    ]
    print("始点ノード:", start_nodes)

    # ランダムウォークを実行し、始点サーバに戻る確率を計算
    return_probabilities = run_random_walk_with_return(
        adjacency_list, node_to_server, start_nodes, alpha
    )

    # 結果をプロット
    plot_return_probabilities(return_probabilities, alpha)
