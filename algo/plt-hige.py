
"""
実行時間のみのばらつきを求めるプログラム

"""
import re
import matplotlib.pyplot as plt
import os
import re


# 比較するグラフの種類（例: karate）
GRAPH_LIST = []
target_graph = "simple_graph"


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
    execution_pattern = r"Execution Time Stats: \{'min': (\d+), 'q1': ([\d\.]+), 'median': ([\d\.]+), 'q3': ([\d\.]+), 'max': (\d+)\}"

    # フォルダの部分を見つける
    folder_match = re.search(folder_pattern, file_content)

    if folder_match:
        # フォルダのマッチ部分の直後の内容を探索
        folder_start_pos = folder_match.end()  # マッチ部分の終了位置
        search_area = file_content[folder_start_pos:]  # その後の部分を探索

        # Execution Time Stats のマッチを探す
        execution_match = re.search(execution_pattern, search_area)

        if execution_match:
            # マッチした値を辞書にして返す
            return {
                "min": int(execution_match.group(1)),
                "q1": float(execution_match.group(2)),
                "median": float(execution_match.group(3)),
                "q3": float(execution_match.group(4)),
                "max": int(execution_match.group(5)),
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
        print(dir_name)

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
# 各データを抽出してリストにまとめる
boxplot_data = [
    [d["min"], d["q1"], d["median"], d["q3"], d["max"]] for d in execution_time_data
]

# ファイル名（結果に対応するラベルとして使用）
labels = ["nojwt", "jwt with construction", "every time move"]

# 箱ひげ図の作成
plt.figure(figsize=(10, 6))
plt.boxplot(boxplot_data, labels=labels)

# グラフのタイトルとラベルを設定
plt.title(f"Execution Time Comparison for Graph: {target_graph}")
plt.ylabel("Execution Time (nanoseconds)")
plt.xlabel("Files")

# 箱ひげ図を表示
plt.tight_layout()
plt.savefig("./hige-figure/" + target_graph + ".png")
