# import pandas as pd
# import matplotlib.pyplot as plt

# # データを辞書として作成
# data = {
#     "A列": [
#         "karate",
#         "karate",
#         "fb-caltech",
#         "fb-caltech",
#         "ca",
#         "ca",
#         "fb-pages",
#         # "fb-pages",
#         "fb-pages",
#     ],
#     "B列": [
#         "METIS",
#         "my-division",
#         "METIS",
#         "my-division",
#         "METIS",
#         "my-division",
#         "METIS",
#         #
#         "my-division",
#     ],
#     "モジュラリティ": [
#         0.0300,
#         0.2690,
#         0.0200,
#         0.1700,
#         0.8400,
#         0.1130,
#         0.0020,
#         # 0.7000,
#         0.0002,
#     ],
#     "増加率": [
#         45.5700,
#         7.4400,
#         39.4200,
#         11.3300,
#         8.7100,
#         7.4000,
#         3.3100,
#         # 7.5300,
#         5.6900,
#     ],
# }

# # データをDataFrameに変換
# df = pd.DataFrame(data)

# # グラフの設定
# plt.figure(figsize=(12, 6))

# # 各グラフに応じた色の設定
# colors = {"karate": "blue", "fb-caltech": "green", "ca": "red", "fb-pages": "purple"}
# markers = {"METIS": "o", "my-division": "s", "Louvain": "D"}

# # データのプロット
# for graph in df["A列"].unique():
#     # グラフごとのデータをフィルタリング
#     subset = df[df["A列"] == graph]
#     # 点をプロット
#     for i, row in subset.iterrows():
#         plt.scatter(
#             row["モジュラリティ"],
#             row["増加率"],
#             label=f"{row['A列']} - {row['B列']}",
#             marker=markers[row["B列"]],
#             color=colors[graph],
#             s=100,
#         )
#     # 同じグラフ内の点を線で結ぶ
#     plt.plot(
#         subset["モジュラリティ"],
#         subset["増加率"],
#         color=colors[graph],
#         linestyle="--",
#         linewidth=1,
#     )

# # ラベルとタイトル
# plt.xlabel("modularity")
# plt.ylabel("increasing rate")
# plt.title("relationship between modularity and increasing rate")
# plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

# # グラフを表示
# plt.tight_layout()
# plt.savefig("modularity-increase.png")
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# データを辞書として作成
data = {
    "A列": [
        "karate",
        "karate",
        "fb-caltech",
        "fb-caltech",
        "ca",
        "ca",
        "fb-pages",
        "fb-pages",
    ],
    "B列": [
        "METIS",
        "my-division",
        "METIS",
        "my-division",
        "METIS",
        "my-division",
        "METIS",
        "my-division",
    ],
    "モジュラリティ": [0.0300, 0.2690, 0.0200, 0.1700, 0.8400, 0.1130, 0.0020, 0.0002],
    "増加率": [45.5700, 7.4400, 39.4200, 11.3300, 8.7100, 7.4000, 3.3100, 5.6900],
    "モジュラリティ変化率": [None, 8.9667, None, 8.5, None, 7.4336, None, 10],
    "増加率変化比": [None, 0.1633, None, 0.2874, None, 1.1770, None, 0.5817],
}

# データをDataFrameに変換
df = pd.DataFrame(data)

# モジュラリティ変化率と増加率変化比をプロットする準備
plt.figure(figsize=(10, 6))

# 各グラフごとにプロット
for graph in df["A列"].unique():
    subset = df[(df["A列"] == graph) & (df["モジュラリティ変化率"].notnull())]
    plt.plot(
        subset["モジュラリティ変化率"], subset["増加率変化比"], marker="o", label=graph
    )

# ラベルとタイトル
plt.xlabel("rate of change in modularity")
plt.ylabel("rate of change in increasing rate")
plt.title("relationship between rate of change in modularity and increasing rate")
plt.legend()

# グラフを表示
plt.tight_layout()
plt.savefig("modularity-increase-rate.png")
plt.show()
