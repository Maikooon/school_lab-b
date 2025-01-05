# import matplotlib.pyplot as plt

# # データ1
# values1 = [
#     876389875,
#     862620042,
#     981566166,
#     950782875,
#     825115375,
#     816519208,
#     822034375,
#     861014833,
#     844341042,
#     856257875,
#     838894042,
#     805826541,
#     844707834,
#     833064542,
#     992272625,
#     856890208,
#     838156708,
#     873852667,
# ]
# min_values1 = [
#     612537708,
#     591374083,
#     656790791,
#     590908833,
#     586232333,
#     570855208,
#     631842583,
#     653573291,
#     597374333,
# ]
# max_values1 = [
#     1189109542,
#     1208507333,
#     1304121125,
#     1163913334,
#     1158904875,
#     1191654542,
#     1173967708,
#     837343792,
#     845700791,
#     1140776750,
#     865223917,
#     1030778583,
#     984482416,
#     975239875,
# ]

# # データ2
# values2 = [
#     897330459,
#     830395792,
#     845566750,
#     829869000,
#     852827291,
#     1007038916,
#     1021354292,
#     900726792,
#     1024694166,
#     847798000,
#     1024935625,
#     870327917,
#     895643666,
#     880643375,
# ]
# min_values2 = [
#     567503458,
#     543264459,
#     521129208,
#     553947500,
#     607836875,
#     531642042,
#     505665333,
#     571678459,
#     647961459,
#     536885875,
#     596682333,
#     634221500,
#     537015833,
# ]
# max_values2 = [
#     1075634292,
#     944715708,
#     946008333,
#     947482459,
#     878964084,
#     1315719250,
#     1030575750,
#     934255417,
#     1029417917,
# ]

# # データをまとめる
# data = [
#     min_values1,
#     max_values1,  # データ1
#     values1,
#     min_values2,
#     max_values2,  # データ2
#     values2,
# ]

# # ラベルの設定
# labels = [
#     "default",
#     "full access",
#     "grouped access",
#     "default",
#     "full access",
#     "grouped access",
# ]

# # プロット
# plt.figure(figsize=(10, 5))
# # x座標を指定
# positions = [
#     1,
#     2,
#     3,  # グループ1
#     5,
#     6,
#     7,  # グループ2
# ]

# # 箱ひげ図
# plt.boxplot(
#     data,
#     positions=positions,
#     patch_artist=True,
#     labels=labels,
#     boxprops=dict(facecolor="lightgrey", color="grey"),
#     medianprops=dict(color="red", linewidth=1.5),
#     whiskerprops=dict(color="grey", linewidth=1.5),
#     capprops=dict(color="grey", linewidth=1.5),
#     flierprops=dict(marker="o", color="grey", alpha=0.5),
# )

# # タイトルとラベル
# plt.title(
#     "Box Plot for Values, Min Values, and Max Values (Data1 & Data2)", fontsize=14
# )
# plt.ylabel("Value", fontsize=12)
# plt.grid(axis="y", linestyle="--", alpha=0.7)

# # 表示
# plt.tight_layout()
# plt.show()


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
data = [values1, min_values1, max_values1, values2, min_values2, max_values2]
labels = [
    "Values1",
    "Min Values1",
    "Max Values1",
    "Values2",
    "Min Values2",
    "Max Values2",
]

# 平均値を計算
means = [np.mean(dataset) for dataset in data]

# 棒グラフをプロット
plt.figure(figsize=(10, 6))
x = np.arange(len(labels))  # ラベルの位置
plt.bar(x, means, color="lightblue", edgecolor="blue", linewidth=1.5)

# ラベルとタイトル
plt.xticks(x, labels, rotation=45, ha="right")
plt.ylabel("Average Value", fontsize=12)
plt.title("Bar Plot of Average Values", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 数値ラベルを追加
for i, mean in enumerate(means):
    plt.text(i, mean, f"{mean:.0f}", ha="center", va="bottom", fontsize=10)

# レイアウト調整
plt.tight_layout()
plt.show()
