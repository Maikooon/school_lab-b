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
        # "fb-pages",
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
        #
        "my-division",
    ],
    "モジュラリティ": [
        0.0300,
        0.2690,
        0.0200,
        0.1700,
        0.8400,
        0.1130,
        0.0020,
        # 0.7000,
        0.0002,
    ],
    # "増加率": [
    #     45.5700,
    #     7.4400,
    #     39.4200,
    #     11.3300,
    #     8.7100,
    #     7.4000,
    #     3.3100,
    #     # 7.5300,
    #     5.6900,
    # ],
    "増加率": [
        0.9646231635,
        0.9679395282,
        0.829631636,
        0.9636877399,
        0.9844971531,
        0.9904237245,
        0.9981220413,
        0.9967245042,
    ],
}

# データをDataFrameに変換
df = pd.DataFrame(data)

# グラフの設定
plt.figure(figsize=(12, 6))

# 各グラフに応じた色の設定
colors = {"karate": "blue", "fb-caltech": "green", "ca": "red", "fb-pages": "purple"}
markers = {"METIS": "o", "my-division": "s", "Louvain": "D"}

# データのプロット
for graph in df["A列"].unique():
    # グラフごとのデータをフィルタリング
    subset = df[df["A列"] == graph]
    # 点をプロット
    for i, row in subset.iterrows():
        plt.scatter(
            row["モジュラリティ"],
            row["増加率"],
            label=f"{row['A列']} - {row['B列']}",
            marker=markers[row["B列"]],
            color=colors[graph],
            s=100,
        )
    # 同じグラフ内の点を線で結ぶ
    plt.plot(
        subset["モジュラリティ"],
        subset["増加率"],
        color=colors[graph],
        linestyle="--",
        linewidth=1,
    )

# ラベルとタイトル
plt.xlabel("modularity")
plt.ylabel("Increase control rate")
plt.title("relationship between modularity and increasing control rate")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

# グラフを表示
plt.tight_layout()
plt.savefig("modularity-increase-new.png")
plt.show()


# 単一サーバにおけるモジュラリティの変化率と増加率変化比の関係をプロットする
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
#         "my-division",
#     ],
#     "モジュラリティ": [0.0300, 0.2690, 0.0200, 0.1700, 0.8400, 0.1130, 0.0020, 0.0002],
#     "増加率": [45.5700, 7.4400, 39.4200, 11.3300, 8.7100, 7.4000, 3.3100, 5.6900],
#     "モジュラリティ変化率": [None, 8.9667, None, 8.5, None, 7.4336, None, 10],
#     "増加率変化比": [None, 0.1633, None, 0.2874, None, 1.1770, None, 0.5817],
# }

# # データをDataFrameに変換
# df = pd.DataFrame(data)

# # モジュラリティ変化率と増加率変化比をプロットする準備
# plt.figure(figsize=(10, 6))

# # 各グラフごとにプロット
# for graph in df["A列"].unique():
#     subset = df[(df["A列"] == graph) & (df["モジュラリティ変化率"].notnull())]
#     plt.plot(
#         subset["モジュラリティ変化率"], subset["増加率変化比"], marker="o", label=graph
#     )

# # ラベルとタイトル
# plt.xlabel("rate of change in modularity")
# plt.ylabel("rate of change in increasing rate")
# plt.title("relationship between rate of change in modularity and increasing rate")
# plt.legend()

# # グラフを表示
# plt.tight_layout()
# plt.savefig("modularity-increase-rate.png")
# plt.show()


# # 分散環境で跨ぎ回数と認証時間の相関があることを示す
# import matplotlib.pyplot as plt
# import numpy as np

# # データの定義
# upward_movement = [77.64, 72.35, 60.15, 56.74, 103.36]
# cross_count = [0.57, 0.45, 0.41, 0.12, 0.62]

# # 分割方法を統一したときの結果
# # upward_movement = [77.64, 60.15, 56.74, 103.36]
# # cross_count = [0.57, 0.41, 0.12, 0.62]

# # 分割方法を統一したときの結果
# # upward_movement = [72.35, 98.61]
# # cross_count = [0.45, 0.41]

# # numpyの配列に変換し、None（無効値）をマスク
# upward_movement = np.array(upward_movement, dtype=np.float64)
# cross_count = np.array(cross_count, dtype=np.float64)

# # 散布図のプロット
# plt.figure(figsize=(8, 6))
# # plt.scatter(upward_movement, cross_count, color="blue", label="Data points")
# plt.scatter(cross_count, upward_movement, color="blue", label="Data points")

# # 各データ点にラベルを追加
# for i, (x, y) in enumerate(zip(upward_movement, cross_count)):
#     if not np.isnan(x) and not np.isnan(y):
#         plt.text(x, y, f"Point {i+1}", fontsize=9, ha="right")

# # 軸ラベルとタイトルの設定
# plt.xlabel("inter-server movement count / rwer")
# plt.ylabel("increasing rate of access time")
# plt.title(
#     "Correlation between upward movement count and increasing rate of access time"
# )
# plt.legend()

# # グラフの表示
# plt.grid(True)
# plt.savefig("upward-crosscount.png")
# plt.show()
