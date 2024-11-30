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
    "no-verify": "./[0]検証なし/cache.txt",
    "verify-every-time": "./[1]毎回検証/cache.txt",
    "add-new-server": "./[2]新サーバを考慮/cache.txt",
}

time_files = {
    "0.01": "./[3]期限あり/0.01-cache.txt",
    "0.05": "./[3]期限あり/0.05-cache.txt",
    "0.075": "./[3]期限あり/0.075-cache.txt",
    "0.1": "./[3]期限あり/0.1-cache.txt",
    "0.125": "./[3]期限あり/0.125-cache.txt",
    "0.15": "./[3]期限あり/0.15-cache.txt",
}

total_move_time_results = []


def extract_move_time(files):
    for label, path in files.items():
        move_time_total = []
        # またぎ回数が200ー300のもののみ抜き出す
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "処理時間:" in line:
                    move_time = float(line.split(":")[1].split(" ")[1])
                    move_time_total.append(move_time)
            total_move_time_results.append(move_time_total)

    # print(total_move_time_results)
    return total_move_time_results


# ここで有効期限別に入れていく
def extract_valid_time(files):
    move_time_total = []
    with open(files, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "処理時間:" in line:
                move_time = float(line.split(":")[1].split(" ")[1])
                move_time_total.append(move_time)
    # 　有効時間を変更した時のy軸の配列がかえる
    return move_time_total


# ここから図表の描画
"""
図表の描画
"""


# 0.01,0.5,0.1,0.15
def plt_picture(move_array, file1, file2, file3, file4, file5, file6):
    plt.figure()
    # カラーマップを設定
    colors = plt.cm.tab10(
        range(len(move_array) + 9)
    )  # データセットごとに異なる色を取得

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
            0.0,
            0.20,
            colors=colors[i],
            linestyles="dashed",
            # label=f"{list(files.keys())[i]} (avg)",
        )

    # ここに有効時間ごとの結果を入れる
    # ファイルの数だけ繰り返す
    x_values = [0.01] * len(file1)
    y_values = file1
    plt.scatter(x_values, y_values, label="0.1 (points)", color=colors[4], s=10)

    x_values = [0.05] * len(file2)
    y_values = file2
    plt.scatter(x_values, y_values, label="0.01 (points)", color=colors[5], s=10)

    x_values = [0.075] * len(file3)
    y_values = file3
    plt.scatter(x_values, y_values, label="0.075 (points)", color=colors[6], s=10)

    x_values = [0.1] * len(file4)
    y_values = file4
    plt.scatter(x_values, y_values, label="0.01 (points)", color=colors[7], s=10)

    x_values = [0.125] * len(file5)
    y_values = file5
    plt.scatter(x_values, y_values, label="0.125 (points)", color=colors[8], s=10)

    x_values = [0.15] * len(file6)
    y_values = file6
    plt.scatter(x_values, y_values, label="0.15 (points)", color=colors[9], s=10)

    # 軸ラベル、凡例、タイトルの設定
    plt.xlabel("Validity time")
    plt.ylabel("1RW move time (s)")
    # plt.xticks(range(len(move_time_results)), labels=move_time_results.keys())
    plt.legend(fontsize=6)
    plt.title("Move Times of 1RW")
    plt.grid(alpha=0.3)
    plt.savefig("[1]valid_time.png")
    plt.show()


if __name__ == "__main__":
    total_move_time_results = extract_move_time(files)
    # 0.0001
    time_01 = extract_valid_time(time_files["0.01"])
    time_005 = extract_valid_time(time_files["0.05"])
    time_0075 = extract_valid_time(time_files["0.075"])
    time_01 = extract_valid_time(time_files["0.1"])
    time_0125 = extract_valid_time(time_files["0.125"])
    time_015 = extract_valid_time(time_files["0.15"])
    plt_picture(
        total_move_time_results,
        time_01,
        time_005,
        time_0075,
        time_01,
        time_0125,
        time_015,
    )
