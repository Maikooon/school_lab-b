import random
import numpy as np
from collections import defaultdict
import os
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

"""
指定されたサーバに属するすべてのノードからランダムウォークをシミュレートし、
一旦外部に出た後、始点サーバに再び戻ってくる確率の平均を計算する。
この確率は累積確率として計算され、特定のホップ数 "までに" 戻ってくる確率を示す。
"""

# ここで変数を設定する
ALPHA = 0.1  # 終了確率 (例: 10%)
RW_COUNT = 10  # ランダムウォークの回数,それぞれの始点サーバからRW _COUNT回だけ繰り返す
START_SERVER = "10.58.60.03"  # 始点サーバ
# GRAPH_PATH = "./server-data/fb-caltech-connected-copy-4/"  # サーバごとに分かれたファイルが格納されたディレクトリ


def read_server_files(directory):
    """
    指定されたディレクトリ内のすべてのサーバファイルを読み取り、
    左側のノードが記載されているファイルに対応するサーバに属することを記録する。
    """
    adjacency_list = defaultdict(list)
    node_to_server = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # ファイル名からサーバのIPを抽出
        if os.path.isfile(file_path):
            # 例: "Abilene03" → "10.58.60.3"
            if "abilene" in filename:
                server_ip = (
                    "10.58.60."
                    + filename.replace("abilene", "").replace(".txt", "").strip()
                )
            else:
                print(f"Unexpected filename format: {filename}")
                continue

            with open(file_path, "r") as f:
                for line in f:
                    try:
                        # 行を分割してノードペアを取得
                        node_a, node_b, _ = line.strip().split(",")
                        node_a, node_b = int(node_a), int(node_b)
                    except ValueError:
                        print(f"Invalid line format skipped: {line.strip()}")
                        continue

                    # 隣接リストを更新
                    adjacency_list[node_a].append(node_b)
                    adjacency_list[node_b].append(node_a)

                    # 左側のノードはファイルのサーバに属するとして記録
                    node_to_server[node_a] = server_ip

    print("Adjacency List:", dict(adjacency_list))
    print("Node to Server Map:", node_to_server)
    return adjacency_list, node_to_server


def run_random_walk_with_return(
    adjacency_list, node_to_server, start_nodes, alpha, num_walks=RW_COUNT
):
    """
    指定されたサーバに属するすべてのノードからランダムウォークをシミュレートし、
    一旦外部に出た後、始点サーバに再び戻ってくる確率の平均を計算する。
    この確率は累積確率として計算され、特定のホップ数 "までに" 戻ってくる確率を示す。
    """
    # 始点サーバに戻る回数を記録
    total_return_counts = defaultdict(int)  # {ホップ数: 回数}

    for start_node in start_nodes:
        # 各ノードからの戻り回数を記録
        print(f"Start node: {start_node}")
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
        print(f"Return counts: {dict(return_counts)}")
        # 各ノードの戻り回数を累積
        for hop, count in return_counts.items():
            total_return_counts[hop] += count

    # 始点サーバに戻る累積確率を計算
    max_hop = max(total_return_counts.keys()) if total_return_counts else 0
    cumulative_counts = np.zeros(max_hop + 1)

    for hop, count in total_return_counts.items():
        cumulative_counts[hop] = count

    # 累積に変換
    cumulative_counts = np.cumsum(cumulative_counts)

    total_walks = len(start_nodes) * num_walks
    return_probabilities = cumulative_counts / total_walks

    return return_probabilities


def plot_multiple_graphs_return_probabilities(graph_results, alpha):
    """
    複数のグラフについて、始点サーバに戻る累積確率をプロット。
    """
    plt.figure(figsize=(10, 6))

    for graph_name, return_probabilities in graph_results.items():
        hops = range(len(return_probabilities))
        plt.plot(
            hops, return_probabilities, marker="o", label=f"{graph_name} (α={alpha})"
        )

    plt.title(f"Cumulative Return Probabilities to Start Server (α={alpha})")
    plt.xlabel("Hop Number")
    plt.ylabel("Cumulative Return Probability")
    plt.xlim(0, 200)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"return-probabilities-{alpha}.png")
    plt.show()


if __name__ == "__main__":
    # グラフディレクトリ一覧（例として3つのグラフ）
    graph_directories = {
        # "test": "./server-data/test/",
        # "karate(34node)": "./server-data/karate/",
        # "fb-caltech-connected(762)": "./server-data/fb-caltech-connected/",
        # "fb-pages-company(14113)": "./server-data/fb-pages-company/",
        # "ca-grqc-connected": "./server-data/ca-grqc-connected/",
        # "fb-caltech-connected-copy-3": "./server-data/fb-caltech-connected/",
        "fb-caltech-connected-copy/3": "./server-data/fb-caltech-connected-copy/3",
        "fb-caltech-connected-copy/4": "./server-data/fb-caltech-connected-copy/4/",
        "fb-caltech-connected-copy/6": "./server-data/fb-caltech-connected-copy/6/",
        "fb-caltech-connected-copy/8": "./server-data/fb-caltech-connected-copy/8/",
        "fb-caltech-connected-copy/10": "./server-data/fb-caltech-connected-copy/10/",
    }

    # 結果を格納する辞書
    graph_results = {}

    # 各グラフで実験
    for graph_name, server_directory in graph_directories.items():
        print(f"Processing {graph_name}...")

        # 隣接リストとサーバ情報を読み取る
        adjacency_list, node_to_server = read_server_files(server_directory)

        # 始点サーバを指定（例：サーバAに属するノード）
        start_nodes = [
            node for node, server in node_to_server.items() if server == START_SERVER
        ]

        if not start_nodes:
            print(f"Warning: No start nodes found for {START_SERVER} in {graph_name}")
            continue

        # ランダムウォークを実行し、始点サーバに戻る累積確率を計算
        return_probabilities = run_random_walk_with_return(
            adjacency_list, node_to_server, start_nodes, ALPHA
        )

        # 結果を辞書に格納
        graph_results[graph_name] = return_probabilities

    # 結果をプロット
    plot_multiple_graphs_return_probabilities(graph_results, ALPHA)
