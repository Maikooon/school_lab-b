"""
結果から箱ひげ図を作成する
"""

import matplotlib.pyplot as plt
import glob

OUTPUT_FILE = "output.txt"

# すべてのファイルのパスを取得 (例: .txtファイル)
file_paths = glob.glob("./../P2P-default/result/karate.txt")

elapsed_times = []

# 各ファイルを読み込み、Elapsed timeをリストに追加
for file_path in file_paths:
    with open(file_path, "r") as f:
        times = []
        for line in f:
            if "Elapsed time" in line:
                time_value = float(line.split(":")[1].strip())
                times.append(time_value)
        elapsed_times.append(times)

# 箱ひげ図を縦方向に描画
plt.figure(figsize=(10, 6))
plt.boxplot(elapsed_times, vert=True, patch_artist=True)
plt.title("Elapsed Time Boxplot for Multiple Files")
plt.xlabel("File index")
plt.ylabel("Time (seconds)")

# ファイルごとのラベルを設定（例としてファイル番号）
plt.xticks(
    ticks=range(1, len(file_paths) + 1),
    labels=[f"File {i+1}" for i in range(len(file_paths))],
)

# 図を表示
plt.show()
