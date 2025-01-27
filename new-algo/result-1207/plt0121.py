import numpy as np
import matplotlib.pyplot as plt

# 各棒のデータセット（4本分）
min_values = [0.6, 0.6, 0.809, 0.809]  # default
mid_values = [0.87, 0.87, 1.04, 1.04]  # 各棒に対する中間値
max_values = [1.54, 1.02, 1.626, 1.2158]  # 各棒に対する最大値

# 既存、改善後、既存、改善後
# x 軸の位置
x_positions = np.array([0, 1, 3, 4])  # 前半2本: 0,1 / 後半2本: 3,4 (間にギャップを設定)

# カラーマップ（min, mid, max に対応する色）
colormap = ["#D3D3D3", "#1E3A8A", "#DC2626"]

# グラフの描画
plt.figure(figsize=(9, 6))

# 各棒をプロット
for i, (min_val, mid_val, max_val, x_pos) in enumerate(
    zip(min_values, mid_values, max_values, x_positions)
):
    # min 部分
    plt.bar(
        x_pos,
        min_val,
        color=colormap[0],
        width=0.8,
        label="min" if i == 0 else None,
    )
    # mid 部分
    plt.bar(
        x_pos,
        mid_val - min_val,
        bottom=min_val,
        color=colormap[1],
        width=0.8,
        label="mid" if i == 0 else None,
    )
    # max 部分
    plt.bar(
        x_pos,
        max_val - mid_val,
        bottom=mid_val,
        color=colormap[2],
        width=0.8,
        label="max" if i == 0 else None,
    )

# x 軸のラベル
plt.xticks(
    x_positions,
    [
        "ca-gqrc-connected [general method]",
        "[proposal method]",
        "com-amazon-connected [general method]",
        "[proposal method]",
    ],
    rotation=15,
    ha="right",
    fontsize=10,
)

# y 軸のラベル
plt.ylabel("Average Execution Time (seconds)", fontsize=12)

# グリッド設定
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 凡例
handles = [plt.Line2D([0], [0], color=color, lw=5) for color in colormap]
plt.legend(
    handles,
    ["no-access-control", "authorization time", "authorization time"],
    loc="upper right",
    fontsize=10,
)

# レイアウト調整
plt.tight_layout()

# 保存と表示
plt.savefig("bar_graph_individual_midpoints.png")
plt.savefig("bar_graph_individual_midpoints.pdf")
plt.show()
