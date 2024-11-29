"""
このスクリプトでは、平均またぎ回数が２−３回ほどのときの、時間の抽出したのちに、プロットする
縦軸が時間で横軸は考慮しない
三本の平行線のようなグラフが描けると思う

処理したいファイル
default/100-log.txt
first-time/100-log.txt    
parent-token/100-log.txt

"""

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
        # またぎ回数が200ー300のもののみ抜き出す
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "total execution time:" in line:
                    move_time = float(line.split(":")[1].split(" ")[1])
                if "サーバのまたぎ回数:" in line:
                    # 　回数が200-300だったら
                    if 200 <= int(line.split(":")[1].strip()) <= 300:
                        print("またぎ回数が200-300のもの")
                        print(move_time)
                        move_time_total.append(move_time)
            total_move_time_results.append(move_time_total)

    # print(total_move_time_results)
    return total_move_time_results


# ここから図表の描画
"""
図表の描画
"""


def plt_picture(move_array):
    plt.figure()
    # カラーマップを設定
    colors = plt.cm.tab10(range(len(move_array)))  # データセットごとに異なる色を取得

    # 各 `move_array` のデータをプロット
    for i, move_time_results in enumerate(move_array):
        x_values = [0] * len(move_time_results)  # x 軸の値は固定
        y_values = move_time_results  # y 軸に配列の値を設定
        plt.scatter(
            x_values,
            y_values,
            label=f"{list(files.keys())[i]} (points)",
            color=colors[i],
            s=10,
        )  # 散布点をプロット

        # 平均値を計算
        avg_y = np.mean(y_values)

        # 平均値の線を描画
        plt.hlines(
            avg_y,
            -0.5,
            10,
            colors=colors[i],
            linestyles="dashed",
            # label=f"{list(files.keys())[i]} (avg)",
        )
    ## 期限付きのデータ
    # 提供された独立したデータをプロット
    x = [
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
    y = [
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
    plt.scatter(
        x,
        y,
        label="parent-token with valid time",
        color="purple",
        s=10,
    )

    # 軸ラベル、凡例、タイトルの設定
    plt.xlabel("length of valid time(s)")
    plt.ylabel("100RW move time (s)")
    # plt.xticks(range(len(move_time_results)), labels=move_time_results.keys())
    plt.legend()
    plt.title("Move Times Across Different Datasets (with Independent Data)")
    plt.grid(alpha=0.3)
    plt.savefig("[100]valid_time.png")
    plt.show()


if __name__ == "__main__":
    total_move_time_results = extract_move_time(files)
    plt_picture(total_move_time_results)
