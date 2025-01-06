import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


# Data points
total_check_count = [0, 11734, 22582, 33819, 45463, 55815, 56426, 57145, 1000321458]
execution_time_ns = [
    763198166,
    1261354959,
    1906780541,
    2751929750,
    4519731875,
    5203566000,
    4562002709,
    4626312625,
]


total_check_count = [
    5587,
    11380,
    17051,
    29582,
    33795,
    45528,
    57014,
    57257,
    23065,
    34429,
    34183,
    44983,
    39846,
]
execution_time_ns = [
    818814958,
    802310291,
    802831750,
    890328916,
    1169057583,
    1137039125,
    1355443666,
    1339727958,
    1021872708,
    927965583,
    927965583,
    1308466208,
    1080824208,
]


# Convert execution time from nanoseconds to seconds for better readability
execution_time_sec = [t / 1e9 for t in execution_time_ns]

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.scatter(total_check_count, execution_time_sec, color="blue", label="Data Points")
# plt.plot(
#     total_check_count,
#     execution_time_sec,
#     linestyle="--",
#     color="blue",
#     label="Trend Line",
# )
# 線形回帰（一次回帰）
coefficients = np.polyfit(total_check_count, execution_time_sec, 1)  # 1次多項式
linear_model = np.poly1d(coefficients)
# プロット用のx軸データを生成（滑らかな曲線にするため）
x_smooth = np.linspace(min(total_check_count), max(total_check_count), 500)
y_smooth = linear_model(x_smooth)

# プロット
plt.scatter(
    total_check_count, execution_time_sec, color="blue", label="Data Points"
)  # 実データ
plt.plot(
    x_smooth, y_smooth, linestyle="--", color="blue", label="Fitted Curve"
)  # 近似曲線

# 線形回帰を計算
slope, intercept, r_value, p_value, std_err = linregress(
    total_check_count, execution_time_sec
)

# 結果を表示
print(f"傾き (slope): {slope:.5e}")
print(f"切片 (intercept): {intercept:.5f}")
print(f"相関係数 (R): {r_value:.5f}")


plt.title("Program Execution Time vs Total Check Count")
plt.xlabel("Total across nodes count")
plt.ylabel("Program Execution Time (seconds)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.savefig("*execution_time_vs_total_check_count.png")
plt.show()
