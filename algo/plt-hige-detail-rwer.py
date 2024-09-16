"""
    1rwerあたりの実行時間のひげずを求めるためのプログラム
"""

import re
import matplotlib.pyplot as plt
import os
import re
import pandas as pd


# 比較するグラフの種類（例: karate）
GRAPH_LIST = [
    "karate",
    "karate-graph",
    "cum",
    "ca-grqc-connected",
    "rt-retweet",
    "tmp",
    "fb-caltech-connected",
    "simple_graph",
]
target_graph = GRAPH_LIST[6]


def extract_execution_time_stats_for_graph(file_content, target_graph, dir_name):
    # フォルダパターンを設定（フォルダの処理部分を特定）
    folder_pattern = (
        r"Processing folder: \./"
        + re.escape(dir_name)
        + r"/result/"
        + re.escape(target_graph)
        + r"/"
    )

    # Execution Time Stats のパターン（正規表現）

    # execution_pattern = r"Execution Time Stats: \{'min': (\d+), 'q1': ([\d\.]+), 'median': ([\d\.]+), 'q3': ([\d\.]+), 'max': (\d+)\}"
    # token_generate_pattern = r"Token Generate Time Stats: \{'min': (\d+), 'q1': ([\d\.]+), 'median': ([\d\.]+), 'q3': ([\d\.]+), 'max': (\d+)\}"
    # token_authenticate_pattern = r"Token Authenticate Time Stats: \{'min': (\d+), 'q1': ([\d\.]+), 'median': ([\d\.]+), 'q3': ([\d\.]+), 'max': (\d+)\}"
    exec_time_per_rwer_pattern = r"Average Time Per Node Stats: \{'min': ([\d\.]+), 'q1': ([\d\.]+), 'median': ([\d\.]+), 'q3': ([\d\.]+), 'max': ([\d\.]+)\}"
    # フォルダの部分を見つける
    folder_match = re.search(folder_pattern, file_content)

    if folder_match:
        # フォルダのマッチ部分の直後の内容を探索
        folder_start_pos = folder_match.end()  # マッチ部分の終了位置
        search_area = file_content[folder_start_pos:]  # その後の部分を探索

        # Execution Time Stats のマッチを探す
        exec_time_per_rwer = re.search(exec_time_per_rwer_pattern, search_area)

        if exec_time_per_rwer:
            # マッチした値を辞書にして返す
            return {
                "exec_time_per_rwer": {
                    "min": float(exec_time_per_rwer.group(1)),
                    "q1": float(exec_time_per_rwer.group(2)),
                    "median": float(exec_time_per_rwer.group(3)),
                    "q3": float(exec_time_per_rwer.group(4)),
                    "max": float(exec_time_per_rwer.group(5)),
                },
            }

    # フォルダが見つからなかった場合、またはExecution Time Statsが見つからなかった場合
    return None


# 複数のファイルから同じグラフの実行時間データを読み込む
def compare_execution_time_across_files(file_paths, target_graph):
    graph_execution_times = []

    for file_path in file_paths:
        with open(file_path, "r") as file:
            content = file.read()
        dir_name = os.path.basename(os.path.dirname(os.path.dirname(file_path)))

        # 指定されたグラフの実行時間を抽出
        execution_time = extract_execution_time_stats_for_graph(
            content, target_graph, dir_name
        )
        if execution_time:
            graph_execution_times.append(execution_time)
    print(graph_execution_times)

    return graph_execution_times


# ファイルリスト
file_paths = [
    "./nojwt/result/folder_stats.txt",
    "./default-jwt/result/folder_stats.txt",
    "./every-time-construction/result/folder_stats.txt",
]

# 各ファイルから同じ種類のグラフの実行時間データを抽出
execution_time_data = compare_execution_time_across_files(file_paths, target_graph)


# データを準備する関数
def prepare_data(data, label):
    formatted_data = []
    for d in data:
        for key, value in d.items():
            formatted_data.append(
                [
                    label + " " + key.replace("_", " "),
                    value["min"],
                    value["q1"],
                    value["median"],
                    value["q3"],
                    value["max"],
                ]
            )
    print(formatted_data)
    return formatted_data


# データフレーム作成

df1 = pd.DataFrame(
    prepare_data([execution_time_data[0]], "no jwt"),
    columns=["metric", "min", "q1", "median", "q3", "max"],
)

df2 = pd.DataFrame(
    prepare_data([execution_time_data[1]], "default jwt"),
    columns=["metric", "min", "q1", "median", "q3", "max"],
)
df3 = pd.DataFrame(
    prepare_data([execution_time_data[2]], "every-time jwt"),
    columns=["metric", "min", "q1", "median", "q3", "max"],
)

df = pd.concat([df1, df2, df3])

gap = 1  # スペースの大きさ
positions = []

# インデックスをカスタマイズしてx軸の位置を決定
for i in range(len(df)):
    if i < 3:
        positions.append(i)  # 前半はそのまま
    else:
        positions.append(i + gap)  # 後半にスペースを加える

# 描画部分
for i, (index, row) in enumerate(df.iterrows()):
    x = positions[i]
    plt.plot([x, x], [row["min"], row["max"]], color="black")  # ヒゲ
    plt.plot([x, x], [row["q1"], row["q3"]], color="black", linewidth=6)  # 四角の部分
    plt.scatter(
        [x], [row["median"]], color="white", edgecolor="black", zorder=3
    )  # 中央値

plt.ylim(0, 1000000)
# ラベルの設定
plt.xticks(positions, df["metric"], rotation=45, ha="right")
plt.title(target_graph + ": Execution, Token Generate, and Token Authenticate Times")
plt.ylabel("Time (ns)")
plt.grid(True)

plt.tight_layout()
plt.savefig("./research/per-Rwer/" + target_graph + ".png")
