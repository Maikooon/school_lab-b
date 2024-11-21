# """
# 実験１
# 増加抑制率とグラフサイズの相関を調べる
# ノード数が大きくなるほど、抑制率も上がることを証明
# """

# import matplotlib.pyplot as plt
# import numpy as np
# from scipy import stats


# # データの定義
# x_values = np.array([762, 4158, 14113])
# y_values = np.array([0.829631636, 0.984497153, 0.998122041])

# # 線形回帰を計算
# slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
# line = slope * x_values + intercept  # 近似直線

# # R^2 値の計算
# r_squared = r_value**2

# # 散布図の作成
# plt.figure(figsize=(8, 6))
# plt.scatter(x_values, y_values, color="blue", label="Data points")
# plt.plot(x_values, line, color="red", label=f"Fit line (R²={r_squared:.4f})")

# # 軸ラベルとタイトルの設定
# plt.xlabel("node size")
# plt.ylabel("increasing control rate")
# plt.title("Suppression rate by number of nodes and grouping")

# # グリッドの追加
# plt.grid(True)
# plt.legend()
# plt.savefig("suppression-rate-by-node-size.png")

# # プロット表示
# plt.show()


"""
NGノードの割合を変化させたtときの
ノード数と抑制率の大きさを示す散布図を作成する
→ノード数が大きくなると、抑制率が牽制される
3
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# データの定義
x_values = np.array([762, 4158, 14113])
y_values = np.array([0.8459359069, 0.9878874469, 0.99832309452])

# 線形回帰を計算
slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
line = slope * x_values + intercept  # 近似直線

# R^2 値の計算
r_squared = r_value**2

# 散布図の作成
plt.figure(figsize=(8, 6))
plt.scatter(x_values, y_values, color="blue", label="Data points")
plt.plot(x_values, line, color="red", label=f"Fit line (R²={r_squared:.4f})")

# 軸ラベルとタイトルの設定
plt.xlabel("node size")
plt.ylabel("increasing control rate")
plt.title("[ng nodes]Suppression rate by number of nodes and grouping")

# グリッドの追加
plt.grid(True)
plt.legend()
plt.savefig("ng-nodes-suppression-rate-by-node-size.png")

# プロット表示
plt.show()
