import numpy as np
import matplotlib.pyplot as plt

# データセット
values1 = [0.6101654625555556]
# min_values_ca_3 = [963906113]
# min_values_ca_2 = [933158188]
min_values_ca_1 = [0.959724462]
max_values1 = [1.5589678625555556]

values2 = [0.809225145]
# min_values_com_3 = [1156564020]
# min_values_com_2 = [1104129288]
min_values_com_1 = [1.168942190]
max_values2 = [1.62625555556]


# mid_height = 0.27297544
# top_height = 0.57582696
# bottom_height 0.6101654625555556

# データとラベル
data = [
    values1,
    max_values1,
    # min_values_ca_3,
    # min_values_ca_2,
    min_values_ca_1,
    values2,
    # min_values_com_3,
    # min_values_com_2,
    max_values2,
    min_values_com_1,
]
# 全てのデータを1000000000で割る
# data = [[x / 1000000000 for x in dataset] for dataset in data]
labels = [
    "no access control",
    "general method",
    "proposed method",
    # "group access(40)",
    # "group access(20)",
]
# colormap = ["grey", "blue", "red", "grey", "blue", "red"]
# colormap = ["#A9A9A9", "#5D8AA8", "#C72C48", "#A9A9A9", "#5D8AA8", "#C72C48"]
# colormap = [
#     "#D3D3D3",
#     "#1E3A8A",
#     "#DC2626",
#     "#FECACA",  # 淡い赤
#     "#F87171",  # 中程度の赤
#     # "#DC2626",  # 鮮やかな赤
#     # "#B91C1C",  # 濃い赤
#     # red,orange,greenみたいにする
#     "#D3D3D3",
#     "#1E3A8A",
#     "#DC2626",
#     "#FECACA",  # 淡い赤
#     "#F87171",  # 中程度の赤
# ]
colormap = [
    "#D3D3D3",
    "#1E3A8A",
    "#DC2626",
    "#D3D3D3",
    "#1E3A8A",
    "#DC2626",
]

# 平均値を計算
means = [np.mean(dataset) for dataset in data]

# x 軸の位置を調整
# x軸の位置を調整
gap = 1
x_front = np.arange(0, len(means) // 2)  # 前半部分
x_back = np.arange(
    len(means) // 2 + gap,
    len(means) + gap,
)  # 後半部分
print(x_front)
print(x_back)
# 棒グラフをプロット
plt.figure(figsize=(8, 5))

# 前半の棒グラフ
for i in range(3):
    print(i)
    print(x_front[i])
    print(means[i])
    plt.bar(
        x_front[i],
        means[i],
        color=colormap[i],
        # edgecolor="grey",
        width=0.9,
        linewidth=0.1,
    )

# # 後半の棒グラフ
for i in range(3, 6):
    print("mmmmm", i)
    print(i)
    print(x_back[i - 3])
    print(means[i])
    plt.bar(
        x_back[i - 3],
        means[i],
        color=colormap[i],
        width=0.9,
        # edgecolor="grey",
        linewidth=1,
    )

# x 軸のラベルを設定
plt.xticks(
    [2, 6],
    ["ca-grqc-connected", "com-amazon-connected"],
    rotation=0,
    ha="right",
    fontsize=12,
)  # 前半と後半に「A」と「B」

# ラベルとタイトル
plt.ylabel("Average Execution time(seconds)", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 凡例を右上に追加
handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colormap]
plt.legend(handles, labels, loc="upper right", fontsize=10)

# レイアウト調整
plt.tight_layout()
plt.savefig("plt0.png")
plt.savefig("plt0.pdf")
plt.show()
