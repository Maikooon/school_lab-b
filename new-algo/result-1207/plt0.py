import numpy as np
import matplotlib.pyplot as plt

# データセット
values1 = [
    876389875,
    862620042,
    981566166,
    950782875,
    825115375,
    816519208,
    822034375,
    861014833,
    844341042,
    856257875,
    838894042,
    805826541,
    844707834,
    833064542,
    992272625,
    856890208,
    838156708,
    873852667,
]
min_values1 = [
    612537708,
    591374083,
    656790791,
    590908833,
    586232333,
    570855208,
    631842583,
    653573291,
    597374333,
]
max_values1 = [
    1189109542,
    1208507333,
    1304121125,
    1163913334,
    1158904875,
    1191654542,
    1173967708,
    837343792,
    845700791,
    1140776750,
    865223917,
    1030778583,
    984482416,
    975239875,
]
values2 = [
    897330459,
    830395792,
    845566750,
    829869000,
    852827291,
    1007038916,
    1021354292,
    900726792,
    1024694166,
    847798000,
    1024935625,
    870327917,
    895643666,
    880643375,
]
min_values2 = [
    567503458,
    543264459,
    521129208,
    553947500,
    607836875,
    531642042,
    505665333,
    571678459,
    647961459,
    536885875,
    596682333,
    634221500,
    537015833,
]
max_values2 = [
    1075634292,
    944715708,
    946008333,
    947482459,
    878964084,
    1315719250,
    1030575750,
    934255417,
    1029417917,
]

# データとラベル
data = [min_values1, max_values1, values1, min_values2, max_values2, values2]
# 全てのデータを1000000000で割る
data = [[x / 1000000000 for x in dataset] for dataset in data]
labels = [
    "default",
    "full access",
    "group access",
]
# colormap = ["grey", "blue", "red", "grey", "blue", "red"]
# colormap = ["#A9A9A9", "#5D8AA8", "#C72C48", "#A9A9A9", "#5D8AA8", "#C72C48"]
colormap = ["#D3D3D3", "#1E3A8A", "#DC2626", "#D3D3D3", "#1E3A8A", "#DC2626"]

# 平均値を計算
means = [np.mean(dataset) for dataset in data]

# x 軸の位置を調整
x_front = np.arange(0, 3)  # 前半の3本
x_back = np.arange(4, 7)  # 後半の3本

# 棒グラフをプロット
plt.figure(figsize=(8, 5))

# 前半の棒グラフ
for i in range(3):
    plt.bar(
        x_front[i],
        means[i],
        color=colormap[i],
        # edgecolor="grey",
        linewidth=1.5,
    )

# 後半の棒グラフ
for i in range(3, 6):
    plt.bar(
        x_back[i - 3],
        means[i],
        color=colormap[i],
        # edgecolor="grey",
        linewidth=1.5,
    )

# x 軸のラベルを設定
plt.xticks(
    [1, 5],
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
plt.show()
