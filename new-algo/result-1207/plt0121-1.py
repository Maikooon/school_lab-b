import numpy as np
import matplotlib.pyplot as plt

# 各棒のデータセット（4本分）#ここの配列のながさを長くしていくことで対応可能
# min_values = [0.6, 0.6, 0.6, 0.6, 0.809, 0.809, 0.809, 0.809]  # default
# mid_values = [0.87, 0.87, 0.87, 0.87, 1.04, 1.04, 1.04, 1.04]  # 各棒に対する中間値
# max_values = [
#     1.54,
#     1.37,
#     1.07,
#     1.02,
#     1.626,
#     1.4674,
#     1.27,
#     1.23,
# ]  # 各棒に対する最大値

min_values = [11.04, 21.96, 4.67, 13.04, 21.90, 3.67]  # default
mid_values = [0, 21.90, 0, 0, 21.90, 0]  # default
max_values = [0, 0, 4.67, 0, 0, 3.67]  # default

# 既存、改善後、既存、改善後
# x 軸の位置
x_positions = np.array(
    [0, 1, 2, 4, 5, 6]
)  # 前半2本: 0,1 / 後半2本: 3,4 (間にギャップを設定)

# カラーマップ（min, mid, max に対応する色）
colormap = ["#F4C2C2", "#E57373", "#CFA7A7"]

# グラフの描画
plt.figure(figsize=(6, 5))

# 各棒をプロット
# for i, (min_val, mid_val, max_val, x_pos) in enumerate(
#     zip(min_values, mid_values, max_values, x_positions)
# ):
# min 部分
plt.bar(
    0,
    min_values[0],
    color=colormap[0],
    width=0.8,
    label="min",
)
plt.bar(
    1,
    min_values[1],
    color=colormap[1],
    width=0.8,
    label="min",
)
plt.bar(
    2,
    min_values[2],
    color=colormap[2],
    width=0.8,
    label="min",
)

plt.bar(
    4,
    min_values[3],
    color=colormap[0],
    width=0.8,
    label="min",
)
plt.bar(
    5,
    min_values[4],
    color=colormap[1],
    width=0.8,
    label="min",
)
plt.bar(
    6,
    min_values[5],
    color=colormap[2],
    width=0.8,
    label="min",
)
# mid 部分
# plt.bar(
#     x_pos,
#     mid_val - min_val,
#     bottom=min_val,
#     color=colormap[1],
#     width=0.8,
#     label="mid" if i == 0 else None,
# )
# # max 部分
# plt.bar(
#     x_pos,
#     max_val - mid_val,
#     bottom=mid_val,
#     color=colormap[2],
#     width=0.8,
#     label="max" if i == 0 else None,
# )

# x 軸のラベル
plt.xticks(
    x_positions,
    [
        "a1",
        "a2",
        "b",
        "a1",
        "a2",
        "b",
    ],
    rotation=0,
    ha="right",
    fontsize=10,
)

# y 軸のラベル
plt.ylabel("Reduction rate from existing(%)", fontsize=12)
plt.xlabel("Added ideas", fontsize=12)

# グリッド設定
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 凡例
handles = [plt.Line2D([0], [0], color=color, lw=5) for color in colormap]
# plt.legend(
#     handles,
#     ["no-access-control", "authorization time", "authorization time"],
#     loc="upper right",
#     fontsize=10,
# )

# レイアウト調整
plt.tight_layout()
plt.ylim(0, 22)

# 保存と表示
plt.savefig("bar_graph_individual_midpoints.png")
plt.savefig("bar_graph_individual_midpoints.pdf")
plt.show()
