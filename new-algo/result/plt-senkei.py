import re
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


# ファイルからデータを抽出する関数
def extract_data_from_file(file_content):
    total_moves = []
    execution_times = []

    # 正規表現パターンを使用してデータを抽出
    total_moves_pattern = re.compile(r"Total moves across communities: (\d+)")
    execution_time_pattern = re.compile(r"Program execution time: (\d+) nanoseconds")

    total_moves_matches = total_moves_pattern.findall(file_content)
    execution_time_matches = execution_time_pattern.findall(file_content)

    # 整数に変換してリストに追加
    total_moves = [int(move) for move in total_moves_matches]
    execution_times = [int(time) for time in execution_time_matches]

    return total_moves, execution_times


# 与えられたファイルのコンテンツ (例)
file_content = """
Average path length: 6.393
Total moves across communities: 2600
Program execution time: 276632500 nanoseconds

Average path length: 6.124
Total moves across communities: 2380
Program execution time: 222322500 nanoseconds


Average path length: 6.286
Total moves across communities: 2526
Program execution time: 227547542 nanoseconds

Average path length: 6.134
Total moves across communities: 2377
Program execution time: 216754833 nanoseconds

Average path length: 6.392
Total moves across communities: 2528
Program execution time: 229427834 nanoseconds

"""

# データを抽出
total_moves, execution_times = extract_data_from_file(file_content)

# ナノ秒をミリ秒に変換
execution_times_ms = [time / 1e6 for time in execution_times]

# 線形回帰の準備
X = np.array(total_moves).reshape(-1, 1)
y = np.array(execution_times_ms)

# 線形回帰モデルを作成してフィッティング
model = LinearRegression()
model.fit(X, y)

# 回帰線を計算
y_pred = model.predict(X)

# グラフの描画
plt.figure(figsize=(8, 6))
plt.scatter(total_moves, execution_times_ms, color="blue", label="Data Points")
plt.plot(total_moves, y_pred, color="red", label="Regression Line")
plt.xlabel("Total Moves Across Communities")
plt.ylabel("Execution Time (ms)")
plt.title("Linear Relationship Between Total Moves and Execution Time")
plt.legend()
plt.grid(True)

# R^2 スコアを表示
r2_score = model.score(X, y)
plt.text(
    min(total_moves),
    max(execution_times_ms),
    f"R² = {r2_score:.4f}",
    fontsize=12,
    color="red",
)
plt.savefig("./fb-caltech-connected/fb-liner.png")
# グラフを表示
plt.show()

# 傾き（coef_）と切片（intercept_）を表示
print(f"Slope (Coefficient): {model.coef_[0]}")
print(f"Intercept: {model.intercept_}")
print(f"R² Score: {r2_score}")
