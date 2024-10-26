"""
実行時間の差分の内訳を出力する

"""

import matplotlib.pyplot as plt
import numpy as np


GRAPH = "fb"
file1 = f"./{GRAPH}/default.txt"
file2 = f"./{GRAPH}/access.txt"
file3 = f"./{GRAPH}/group-access.txt"


def average(filename):
    total_time = []
    access_time = []
    token_generate_time = []
    toke_verify_time = []

    with open(filename, "r") as file:
        for line in file:
            if "Elapsed time " in line:
                total_time.append(float(line.split()[-1]))
            if "total_determinate_ng_nodes:" in line:
                access_time.append(float(line.split()[-1]))
            if "total_jwt_verify_time:" in line:
                token_generate_time.append(float(line.split()[-1]))
            if "total_jwt_generate:" in line:
                toke_verify_time.append(float(line.split()[-1]))
    print(f"Total time: {total_time}")

    if len(access_time) == 0:
        ave_access_time = sum(access_time)
        ave_token_generate_time = sum(token_generate_time)
        ave_toke_verify_time = sum(toke_verify_time)
    else:
        ave_access_time = sum(access_time) / len(access_time)
        ave_token_generate_time = sum(token_generate_time) / len(token_generate_time)
        ave_toke_verify_time = sum(toke_verify_time) / len(toke_verify_time)

    ave_time = sum(total_time) / len(total_time)
    return ave_time, ave_access_time, ave_token_generate_time, ave_toke_verify_time


if __name__ == "__main__":
    ave_time1, ave_access_time1, ave_token_generate_time1, ave_toke_verify_time1 = (
        average(file1)
    )
    ave_time2, ave_access_time2, ave_token_generate_time2, ave_toke_verify_time2 = (
        average(file2)
    )
    ave_time3, ave_access_time3, ave_token_generate_time3, ave_toke_verify_time3 = (
        average(file3)
    )

    all_access_time = [ave_access_time1, ave_access_time2, ave_access_time3]
    all_token_generate_time = [
        ave_token_generate_time1,
        ave_token_generate_time2,
        ave_token_generate_time3,
    ]
    all_token_verify_time = [
        ave_toke_verify_time1,
        ave_toke_verify_time2,
        ave_toke_verify_time3,
    ]

    labels = ["non-access-limit", "access", "grouped access"]

    # グラフのバー設定
    x = np.arange(len(labels))  # バーの位置
    width = 0.5  # バーの幅

    # スタックバーグラフのプロット
    fig, ax = plt.subplots()
    ax.bar(
        x,
        all_access_time,
        width,
        bottom=0,
        label="Average Access Time",
    )
    ax.bar(
        x,
        all_token_generate_time,
        width,
        bottom=np.array(all_access_time),
        label="Average Token Generate Time",
    )
    ax.bar(
        x,
        all_token_verify_time,
        width,
        bottom=np.array(all_access_time) + np.array(all_token_generate_time),
        label="Average Token Verify Time",
    )

    # ラベルとタイトルの追加
    ax.set_xlabel("Data Set")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Average Time Distribution")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.savefig(f"./{GRAPH}/bar.png")

    plt.show()
