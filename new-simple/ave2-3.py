"""
このスクリプトでは、平均またぎ回数が２−３回ほどのときの、時間の抽出したのちに、プロットする
縦軸が時間で横軸は考慮しない
三本の平行線のようなグラフが描けると思う

処理したいファイル
default/100-log.txt
first-time/100-log.txt
parent-token/100-log.txt
"""

# ここから平均値を求めるグラフ

import matplotlib.pyplot as plt
import numpy as np

files = {
    "no authentication(method-c)": "./default/100-log.txt",
    "proposal-α": "./first-time/100-log.txt",
    "proposal-β": "./parent-token/100-log.txt",
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
    plt.figure(figsize=(8, 6))
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
    data = [[j + 0.6101654625555555 for j in i] for i in data]

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
        y_values = [y + 0.6101654625555555 for y in y_values]
        plt.scatter(
            x_values,
            y_values,
            label=f"{label}",
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
    plt.xlabel("Parent token valid time")
    plt.ylabel("1RW Move Time (seconds)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("[1RW]comparison_valid_plot.pdf")
    plt.show()


if __name__ == "__main__":
    total_move_time_results = extract_move_time(files)
    plt_picture(total_move_time_results)
