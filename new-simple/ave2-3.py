# """
# このスクリプトでは、平均またぎ回数が２−３回ほどのときの、時間の抽出したのちに、プロットする
# 縦軸が時間で横軸は考慮しない
# 三本の平行線のようなグラフが描けると思う

# 処理したいファイル
# default/100-log.txt
# first-time/100-log.txt
# parent-token/100-log.txt

# """

# import matplotlib.pyplot as plt
# import numpy as np

# files = {
#     "default": "./default/100-log.txt",
#     "first-time": "./first-time/100-log.txt",
#     "parent-token": "./parent-token/100-log.txt",
# }

# total_move_time_results = []


# def extract_move_time(files):
#     for label, path in files.items():
#         move_time_total = []
#         # またぎ回数が200ー300のもののみ抜き出す
#         with open(path, "r") as f:
#             lines = f.readlines()
#             for line in lines:
#                 if "total execution time:" in line:
#                     move_time = float(line.split(":")[1].split(" ")[1])
#                 if "サーバのまたぎ回数:" in line:
#                     # 　回数が200-300だったら
#                     if 200 <= int(line.split(":")[1].strip()) <= 300:
#                         print("またぎ回数が200-300のもの")
#                         print(move_time)
#                         move_time_total.append(move_time)
#             total_move_time_results.append(move_time_total)

#     # print(total_move_time_results)
#     return total_move_time_results


# # ここから図表の描画
# """
# 図表の描画
# """


# def plt_picture(move_array):
#     plt.figure()
#     # カラーマップを設定
#     colors = plt.cm.tab10(range(len(move_array)))  # データセットごとに異なる色を取得

#     # 各 `move_array` のデータをプロット
#     for i, move_time_results in enumerate(move_array):
#         x_values = [0] * len(move_time_results)  # x 軸の値は固定
#         y_values = move_time_results  # y 軸に配列の値を設定

#         ## 一RW分の時間で考える
#         y_values = [y / 100 for y in y_values]
#         plt.scatter(
#             x_values,
#             y_values,
#             label=f"{list(files.keys())[i]} (points)",
#             color=colors[i],
#             s=10,
#         )  # 散布点をプロット

#         # 平均値を計算
#         avg_y = np.mean(y_values)

#         # 平均値の線を描画
#         plt.hlines(
#             avg_y,
#             0,
#             0.12,
#             colors=colors[i],
#             linestyles="dashed",
#             # label=f"{list(files.keys())[i]} (avg)",
#         )
#     ## 期限付きのデータ
#     # 提供された独立したデータをプロット
#     x = [
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0.2,
#         0.2,
#         0.2,
#         0.2,
#         0.5,
#         0.5,
#         0.5,
#         0.5,
#         0.5,
#         0.5,
#         0.5,
#         1,
#         1,
#         1,
#         1,
#         1,
#         1.75,
#         1.75,
#         1.75,
#         1.75,
#         2,
#         2,
#         2,
#         2,
#         2,
#         3,
#         3,
#         3,
#         3,
#         5,
#         5,
#         5,
#         5,
#         5,
#         10,
#         10,
#         10,
#         10,
#         10,
#         10,
#     ]
#     y = [
#         57.876,
#         54.729,
#         54.528,
#         55.25,
#         54.272,
#         55.097,
#         54.944,
#         52.684,
#         48.711642485,
#         54.100127481,
#         53.440346330,
#         48.711642485,
#         34.869,
#         38.634,
#         32.864,
#         35.655,
#         40.32,
#         33.248,
#         34.782,
#         20.626,
#         27.022,
#         23.827,
#         25.895,
#         23.563,
#         17.164,
#         19.365,
#         17.365,
#         17.298,
#         20.077,
#         16.86,
#         19.123,
#         14.243,
#         17.333,
#         17.513,
#         16.165,
#         15.162,
#         15.833,
#         13.098,
#         15.588,
#         14.408,
#         18.319,
#         16.394,
#         13.592,
#         13.567,
#         12.998,
#         15.548,
#         14.291,
#         14.322,
#     ]

#     plt.scatter(
#         x,
#         y,
#         label="parent-token with valid time",
#         color="purple",
#         s=10,
#     )

#     # # 軸ラベル、凡例、タイトルの設定
#     # plt.xlabel("length of valid time(s)")
#     # plt.ylabel("1RW move time (s)")
#     # # plt.xticks(range(len(move_time_results)), labels=move_time_results.keys())
#     # plt.legend()
#     # plt.title("Move Times Across Different Datasets (with Independent Data)")
#     # plt.grid(alpha=0.3)
#     # plt.savefig("[100]valid_time.png")
#     # plt.show()
#     # xとyを100で割ってスケーリング
#     x = [xi / 100 for xi in x]
#     y = [yi / 100 for yi in y]

#     # xのユニークな値ごとにyをグループ化
#     unique_x = sorted(set(x))
#     grouped_y = {ux: [] for ux in unique_x}

#     for xi, yi in zip(x, y):
#         grouped_y[xi].append(yi)

#     # 箱ひげ図用のデータリストを準備
#     data = [grouped_y[ux] for ux in unique_x]

#     # 箱ひげ図を描画
#     fig, ax = plt.subplots(figsize=(10, 6))
#     bp = ax.boxplot(
#         data,
#         vert=True,
#         patch_artist=True,
#         boxprops=dict(facecolor="purple", color="black"),
#         medianprops=dict(color="yellow"),
#     )

#     # x軸ラベルの設定
#     ax.set_xticks(range(1, len(unique_x) + 1))
#     ax.set_xticklabels([f"{ux:.2f}" for ux in unique_x], rotation=45)

#     # ラベルやタイトルの設定
#     ax.set_xlabel("Length of Valid Time (s)")
#     ax.set_ylabel("1RW Move Time (s)")
#     plt.title("Boxplot of Move Times Grouped by Valid Time")
#     plt.grid(alpha=0.3)

#     # グラフを表示
#     plt.show()


# if __name__ == "__main__":
#     total_move_time_results = extract_move_time(files)
#     plt_picture(total_move_time_results)


import matplotlib.pyplot as plt
import numpy as np

files = {
    "default": "./default/100-log.txt",
    "first-time": "./first-time/100-log.txt",
    "parent-token": "./parent-token/100-log.txt",
}

total_move_time_results = []


def extract_move_time(files):
    for label, path in files.items():
        move_time_total = []
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "total execution time:" in line:
                    move_time = float(line.split(":")[1].split(" ")[1])
                if "サーバのまたぎ回数:" in line:
                    if 200 <= int(line.split(":")[1].strip()) <= 300:
                        move_time_total.append(move_time)
            total_move_time_results.append((label, move_time_total))
    return total_move_time_results


def plt_picture(move_array):
    # グラフ設定
    plt.figure(figsize=(12, 8))
    colors = plt.cm.tab10(range(len(move_array)))
    # 追加データのプロット (箱ひげ図)
    x = [
        xi / 100
        for xi in [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0.2,
            0.2,
            0.2,
            0.2,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            1,
            1,
            1,
            1,
            1,
            1.75,
            1.75,
            1.75,
            1.75,
            2,
            2,
            2,
            2,
            2,
            3,
            3,
            3,
            3,
            5,
            5,
            5,
            5,
            5,
            10,
            10,
            10,
            10,
            10,
            10,
        ]
    ]
    y = [
        yi / 100
        for yi in [
            57.876,
            54.729,
            54.528,
            55.25,
            54.272,
            55.097,
            54.944,
            52.684,
            48.711642485,
            54.100127481,
            53.440346330,
            48.711642485,
            34.869,
            38.634,
            32.864,
            35.655,
            40.32,
            33.248,
            34.782,
            20.626,
            27.022,
            23.827,
            25.895,
            23.563,
            17.164,
            19.365,
            17.365,
            17.298,
            20.077,
            16.86,
            19.123,
            14.243,
            17.333,
            17.513,
            16.165,
            15.162,
            15.833,
            13.098,
            15.588,
            14.408,
            18.319,
            16.394,
            13.592,
            13.567,
            12.998,
            15.548,
            14.291,
            14.322,
        ]
    ]
    unique_x = sorted(set(x))
    grouped_y = {ux: [] for ux in unique_x}
    for xi, yi in zip(x, y):
        grouped_y[xi].append(yi)
    data = [grouped_y[ux] for ux in unique_x]

    # 箱ひげ図
    plt.boxplot(
        data,
        # positions=0,  # 横軸位置調整
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor="purple", color="black"),
        medianprops=dict(color="yellow"),
    )
    x_min, x_max = plt.xlim()  # 現在のx軸の範囲を取得
    # データごとのプロット
    for i, (label, move_time_results) in enumerate(move_array):
        x_values = [0] * len(move_time_results)
        y_values = [y / 100 for y in move_time_results]  # スケーリング
        plt.scatter(
            x_values,
            y_values,
            label=f"{label} (scatter)",
            color=colors[i],
            s=15,
            alpha=0.7,
        )
        # plt.hlines(avg_y, i + 0.85, i + 1.15, colors=colors[i], linestyles="dashed")

        # 平均値を計算
        avg_y = np.mean(y_values)

        # 平均値の線を描画
        plt.hlines(
            avg_y,
            0,
            x_max,
            colors=colors[i],
            linestyles="dashed",
            # label=f"{list(files.keys())[i]} (avg)",
        )

    # ラベル設定
    x_labels = [f"{ux:.2f}" for ux in unique_x]
    plt.xticks(range(1, len(x_labels) + 1), x_labels, rotation=45)
    plt.xlabel("Dataset or Valid Time")
    plt.ylabel("1RW Move Time (s)")
    plt.title("Comparison of Move Times")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("[1RW]comparison_valid_plot.png")
    plt.show()


if __name__ == "__main__":
    total_move_time_results = extract_move_time(files)
    plt_picture(total_move_time_results)
